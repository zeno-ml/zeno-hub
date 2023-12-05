"""FastAPI server endpoints for slice-related queries."""
from amplitude import BaseEvent
from fastapi import APIRouter, Depends, HTTPException, Request, status

import zeno_backend.database.delete as delete
import zeno_backend.database.insert as insert
import zeno_backend.database.select as select
import zeno_backend.database.update as update
import zeno_backend.util as util
from zeno_backend.classes.amplitude import AmplitudeHandler
from zeno_backend.classes.base import (
    ZenoColumn,
)
from zeno_backend.classes.slice import Slice
from zeno_backend.classes.slice_finder import SliceFinderRequest, SliceFinderReturn
from zeno_backend.processing.filtering import table_filter
from zeno_backend.processing.slice_finder import slice_finder

router = APIRouter(tags=["zeno"])


@router.get(
    "/slices/{project}",
    response_model=list[Slice],
    tags=["zeno"],
)
async def get_slices(project: str, request: Request):
    """Fetch all slices of a project.

    Args:
        project (str): project to fetch all slices for.
        request (Request): http request to get user information from.

    Returns:
        list[Slice]: requested slices.
    """
    await util.project_access_valid(project, request)
    return await select.slices(project)


@router.post(
    "/slice-finder/{project}",
    tags=["zeno"],
    response_model=SliceFinderReturn,
)
async def run_slice_finder(
    req: SliceFinderRequest,
    project: str,
    request: Request,
    current_user=Depends(util.auth.claim()),
):
    """Run slice finder to recommend slices to the user.

    Args:
        req (SliceFinderRequest): request to slice finder algorithm specifying params.
        project (str): project to run slice finder for.
        request (Request): http request to get user information from.
        current_user (Any, optional): user who initiated the slice finder request.
            Defaults to Depends(util.auth.claim()).

    Returns:
        SliceFinderReturn: the result of the slice finder algorithm.
    """
    await util.project_editor(project, request)
    AmplitudeHandler().track(
        BaseEvent(
            event_type="Ran Slice Finder",
            user_id=current_user["sub"],
            event_properties={"project_uuid": project},
        )
    )
    return await slice_finder(project, req)


@router.post(
    "/slices-for-projects/",
    response_model=list[Slice],
    tags=["zeno"],
)
async def get_slices_for_projects(req: list[str], request: Request):
    """Get all slices for a list of projects.

    Args:
        req (list[str]): the projects to fetch slices for.
        request (Request): http request to get user information from.

    Returns:
        list[Slice]: all slices in all specifiec projects.
    """
    if len(req) == 0:
        return []
    for project in req:
        await util.project_access_valid(project, request)
    return await select.slices_for_projects(req)


@router.post(
    "/slice/{project}",
    response_model=int,
    tags=["zeno"],
)
async def add_slice(
    project: str,
    slice: Slice,
    request: Request,
    current_user=Depends(util.auth.claim()),
):
    """Add a slice to a project.

    Args:
        project (str): project to add the slice to.
        slice (Slice): slice to be added to the project.
        request (Request): http request to get user information from.
        current_user (Any, optional): User who wants to add a slice to a project.
            Defaults to Depends(util.auth.claim()).

    Raises:
        HTTPException: error if adding slice fails.

    Returns:
        int: id of the newly added slice.
    """
    await util.project_editor(project, request)
    id = await insert.slice(project, slice)
    AmplitudeHandler().track(
        BaseEvent(
            event_type="Slice Created",
            user_id=current_user["sub"],
            event_properties={"project_uuid": project},
        )
    )
    return id


@router.post(
    "/slice-instance-ids/{slice_id}/{model}", response_model=list[str], tags=["zeno"]
)
async def get_slice_instance_ids(
    slice_id: int, model: str | None, id_column: ZenoColumn, request: Request
):
    """Get all instance ids of a slice.

    Args:
        slice_id (int): id of the slice to get instance ids for.
        model (str | None): model of the slice.
        id_column (ZenoColumn): column to get ids from.
        request (Request): http request to get user information from.

    Raises:
        HTTPException: error if the project cannot be found.

    Returns:
        list[str]: all ids of the slice.
    """
    slice = await select.slice_by_id(slice_id)
    project_uuid = slice.project_uuid

    if project_uuid is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    await util.project_access_valid(project_uuid, request)

    filter_sql = await table_filter(project_uuid, model, slice.filter_predicates)

    return await select.slice_instance_ids(project_uuid, filter_sql, id_column)


@router.post(
    "/all-slices/{project}",
    response_model=list[int],
    tags=["zeno"],
    dependencies=[Depends(util.auth)],
)
async def add_all_slices(
    project: str, column: ZenoColumn, request: Request, name: str | None = None
):
    """Add all slices for a column's values.

    Args:
        project (str): project to add the slices to.
        column (ZenoColumn): column to add all slices for.
        request (Request): http request to get user information from.
        name (str | None, optional): name of the folder the slices should be added to.
            Defaults to None.

    Raises:
        HTTPException: error if adding slices fails.

    Returns:
        list[int]: ids of all added slices.
    """
    await util.project_editor(project, request)
    try:
        ids = await insert.all_slices_for_column(project, column, name)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
    if ids is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to insert slices",
        )
    return ids


@router.patch("/slice/{project}", tags=["zeno"], dependencies=[Depends(util.auth)])
async def update_slice(slice: Slice, project_uuid: str, request: Request):
    """Update a slice in the database.

    Args:
        slice (Slice): new values of the slice to be updated.
        project_uuid (str): project uuid to which the slice belongs.
        request (Request): http request to get user information from.
    """
    await util.project_editor(project_uuid, request)
    if slice.project_uuid == project_uuid:
        await update.clear_chart_data(project_uuid)
        await update.slice(slice, project_uuid)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.delete(
    "/slice/{project_uuid}/{slice_id}", tags=["zeno"], dependencies=[Depends(util.auth)]
)
async def delete_slice(project_uuid: str, slice_id: int, request: Request):
    """Delete a slice from the database.

    Args:
        project_uuid (str): project to which the slice belongs (to check permissions).
        slice_id (int): id of the slice to be deleted.
        request (Request): http request to get user information from.
    """
    await util.project_editor(project_uuid, request)
    slice = await select.slice_by_id(slice_id)
    if slice.project_uuid == project_uuid:
        await update.clear_chart_data(project_uuid)
        await delete.slice(slice_id)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
