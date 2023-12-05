"""FastAPI server endpoints for report-related queries."""
from urllib import parse

from amplitude import BaseEvent
from fastapi import APIRouter, Depends, HTTPException, Request, status

import zeno_backend.database.delete as delete
import zeno_backend.database.insert as insert
import zeno_backend.database.select as select
import zeno_backend.database.update as update
import zeno_backend.util as util
from zeno_backend.classes.amplitude import AmplitudeHandler
from zeno_backend.classes.report import (
    Report,
    ReportElement,
    ReportResponse,
    SliceElementOptions,
    SliceElementSpec,
    TagElementOptions,
    TagElementSpec,
)
from zeno_backend.classes.user import Organization, User

router = APIRouter(tags=["zeno"])


@router.get(
    "/report-name/{owner_name}/{report_name}",
    response_model=ReportResponse,
    tags=["zeno"],
)
async def get_report_by_name(owner_name: str, report_name: str, request: Request):
    """Get a report by its name and owner name.

    Args:
        owner_name (str): name of the owner of the report.
        report_name (str): name of the report.
        request (Request): http request to get user information from.

    Raises:
        HTTPException: error if the report could not be loaded.

    Returns:
        Report: the requested report.
    """
    report_id = await select.report_id(owner_name, parse.unquote(report_name))
    if report_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
        )
    return get_report(report_id, request)


@router.get("/report/{id}", response_model=ReportResponse, tags=["zeno"])
async def get_report(id: int, request: Request):
    """Get a report by its id.

    Args:
        id (int): unique id of the report.
        request (Request): http request to get user information from.

    Raises:
        HTTPException: error if the report could not be loaded.

    Returns:
        Report: the requested report.
    """
    await util.report_access_valid(id, request)
    return await select.report_response(
        id, user=await util.get_user_from_token(request)
    )


@router.post(
    "/report-elements/{report_id}",
    response_model=list[ReportElement],
    tags=["zeno"],
)
async def get_report_elements(report_id: int, request: Request):
    """Get all elements that a report contains.

    Args:
        report_id (int): id of the report for which to fetch elements.
        request (Request): http request to get user information from.

    Returns:
        list[ReportElement] | None: all elements that a report contains.
    """
    await util.report_access_valid(report_id, request)
    return await select.report_elements(report_id)


@router.post("/like-report/{report_id}", tags=["zeno"])
async def like_report(report_id: int, current_user=Depends(util.auth.claim())):
    """Like a report as a user.

    Args:
        report_id (int): id of the report to be liked by the user.
        current_user (Any, optional): The user who wants to like the report.
            Defaults to Depends(util.auth.claim()).
    """
    user = await select.user(current_user["username"])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    await insert.like_report(user.id, report_id)


@router.get(
    "/report-users/{report_id}",
    response_model=list[User],
    tags=["zeno"],
    dependencies=[Depends(util.auth)],
)
async def get_report_users(report_id: int, request: Request):
    """Get all users  that have access to a report.

    Args:
        report_id (int): the report for which to get user access.
        request (Request): http request to get user information from.

    Returns:
        list[User]: the list of users who can access the report.
    """
    await util.report_editor(report_id, request)
    return await select.report_users(report_id)


@router.get(
    "/report-organizations/{report_id}",
    response_model=list[Organization],
    tags=["zeno"],
    dependencies=[Depends(util.auth)],
)
async def get_report_orgs(report_id: int, request: Request):
    """Get all the organizations that have access to a report.

    Args:
        report_id (int): the report for which to get organization access.
        request (Request): http request to get user information from.

    Returns:
        list[Organization]: the list of organizations who can access the report.
    """
    await util.report_editor(report_id, request)
    return await select.report_orgs(report_id)


@router.post(
    "/slice-element-options/",
    response_model=SliceElementOptions,
    tags=["zeno"],
)
async def get_slice_element_options(
    slice_element_spec: SliceElementSpec, request: Request
):
    """Get the options of a report's slice element.

    Args:
        slice_element_spec (SliceElementSpec): specification of the slice element.
        request (Request): request to get user information from.

    Raises:
        HTTPException: error if slice element options could not be loaded.

    Returns:
        SliceElementOptions | None: options of a report's slice element.
    """
    slice = await select.slice(slice_element_spec.slice_id)
    project_uuid = slice.project_uuid
    if project_uuid is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    await util.project_access_valid(project_uuid, request)

    return await select.slice_element_options(
        slice, project_uuid, slice_element_spec.system_name
    )


@router.post(
    "/tag-element-options/",
    response_model=TagElementOptions,
    tags=["zeno"],
)
async def get_tag_element_options(tag_element_spec: TagElementSpec, request: Request):
    """Get the options of a report's tag element.

    Args:
        tag_element_spec (TagElementSpec): specification of the tag element.
        request (Request): request to get user information from.

    Raises:
        HTTPException: error if tag element options could not be loaded.

    Returns:
        TagElementOptions | None: options of a report's tag element.
    """
    tag = await select.tag(tag_element_spec.tag_id)
    project_uuid = tag.project_uuid
    if project_uuid is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    await util.project_access_valid(project_uuid, request)
    return await select.tag_element_options(
        tag, project_uuid, tag_element_spec.system_name
    )


@router.post("/report/{name}", tags=["zeno"], dependencies=[Depends(util.auth)])
async def add_report(name: str, current_user=Depends(util.auth.claim())):
    """Add a new report to the Database.

    Args:
        name (str): name of the report to be added.
        current_user (Any, optional): The user who wants to add the report.
            Defaults to Depends(util.auth.claim()).

    Raises:
        HTTPException: error if the report could not be added.

    Returns:
        int: id of the newly created report.
    """
    user = await select.user(current_user["username"])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    try:
        id = await insert.report(name, user)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    AmplitudeHandler().track(
        BaseEvent(
            event_type="Report Created",
            user_id=current_user["sub"],
        )
    )
    return id


@router.post("/report-element/{id}", tags=["zeno"], dependencies=[Depends(util.auth)])
async def add_report_element(
    report_id: int,
    element: ReportElement,
    request: Request,
    current_user=Depends(util.auth.claim()),
):
    """Add an element to an existing report.

    Args:
        report_id (int): id of the report to add an element to.
        element (ReportElement): element to be added to the report.
        request (Request): http request to get user information from.
        current_user (Any, optional): user who wants to add an element to a report.
            Defaults to Depends(util.auth.claim()).

    Raises:
        HTTPException: error if adding an element to a report fails.

    Returns:
        id: id of the newly created report element.
    """
    await util.report_editor(report_id, request)
    user = await select.user(current_user["username"])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    id = await insert.report_element(report_id, element)
    if id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to insert report element",
        )
    AmplitudeHandler().track(
        BaseEvent(
            event_type="Report Element Created",
            user_id=current_user["sub"],
            event_properties={"report_id": report_id},
        )
    )
    return id


@router.post(
    "/report-user/{report_id}", tags=["zeno"], dependencies=[Depends(util.auth)]
)
async def add_report_user(report_id: int, user: User, request: Request):
    """Add a user to a report.

    Args:
        report_id (int): report to add the user to.
        user (User): user to be added to the report.
        request (Request): http request to get user information from.
    """
    await util.report_editor(report_id, request)
    report_obj = await select.report_from_id(report_id)
    if report_obj.owner_name != user.name:
        await insert.report_user(report_id, user)


@router.post(
    "/report-org/{report_id}", tags=["zeno"], dependencies=[Depends(util.auth)]
)
async def add_report_org(report_id: int, organization: Organization, request: Request):
    """Add an organization to a report.

    Args:
        report_id (int): report to add the user to.
        organization (Organization): organization to be added to the report.
        request (Request): http request to get user information from.
    """
    await util.report_editor(report_id, request)
    await insert.report_org(report_id, organization)


@router.patch(
    "/report-user/{report_id}", tags=["zeno"], dependencies=[Depends(util.auth)]
)
async def update_report_user(report_id: int, user: User, request: Request):
    """Update a user's privileges for a report.

    Args:
        report_id (int): the report to update user privileges for.
        user (User): updated user privileges.
        request (Request): http request to get user information from.
    """
    await util.report_editor(report_id, request)
    await update.report_user(report_id, user)


@router.patch("/report-org/{project}", tags=["zeno"], dependencies=[Depends(util.auth)])
async def update_report_org(
    report_id: int, organization: Organization, request: Request
):
    """Update a organization's privileges for a report.

    Args:
        report_id (int): the report to update user privileges for.
        organization (Organization): updated organization privileges.
        request (Request): http request to get user information from.
    """
    await util.report_editor(report_id, request)
    await update.report_org(report_id, organization)


@router.patch(
    "/report-element/{report_id}",
    tags=["zeno"],
    dependencies=[Depends(util.auth)],
)
async def update_report_element(
    report_id: int, element: ReportElement, request: Request
):
    """Update an element of a report.

    Args:
        report_id (int): the report to update the element for.
        element (ReportElement): updated report element.
        request (Request): http request to get user information from.
    """
    await util.report_editor(report_id, request)
    await update.report_element(element)


@router.patch("/report/", tags=["zeno"], dependencies=[Depends(util.auth)])
async def update_report(report: Report, request: Request):
    """Update a report's settings.

    Args:
        report (Report): updated report settings.
        request (Request): http request to get user information from.
    """
    await util.report_editor(report.id, request)
    await update.report(report)


@router.patch("/report-projects/", tags=["zeno"], dependencies=[Depends(util.auth)])
async def update_report_projects(
    report_id: int, project_uuids: list[str], request: Request
):
    """Update the projects associated with a report.

    Args:
        report_id (int): the report to update the projects for.
        project_uuids (list[str]): list of project UUIDs associated with the report.
        request (Request): http request to get user information from.
    """
    await util.report_editor(report_id, request)
    await update.report_projects(report_id, project_uuids)


@router.delete("/report/{report_id}", tags=["zeno"])
async def delete_report(report_id: int, current_user=Depends(util.auth.claim())):
    """Delete an existing report from the databse.

    Args:
        report_id (int): the id of the report to be deleted.
        current_user (Any, optional): The user who wants to delete the report.
            Defaults to Depends(util.auth.claim()).

    Raises:
        HTTPException: error if the deletion was not successful.
    """
    report_obj = await select.report_from_id(report_id)
    # make sure only project owners can delete a project
    if report_obj.owner_name != current_user["username"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    await delete.report(report_id)


@router.delete(
    "/report-element/{report_id}/{id}", tags=["zeno"], dependencies=[Depends(util.auth)]
)
async def delete_report_element(report_id: int, id: int, request: Request):
    """Delete an element from a report.

    Args:
        report_id (int): the id of the report the element is associated with.
        id (int): the id of the report element to be deleted.
        request (Request): http request to get user information from.
    """
    await util.report_editor(report_id, request)
    await delete.report_element(id)


@router.delete(
    "/report-user/{report_id}", tags=["zeno"], dependencies=[Depends(util.auth)]
)
async def delete_report_user(report_id: int, user: User, request: Request):
    """Remove a user from a report.

    Args:
        report_id (int): id dof the report to remove a user from.
        user (User): user to be removed from the report.
        request (Request): http request to get user information from.
    """
    await util.report_editor(report_id, request)
    await delete.report_user(report_id, user)


@router.delete(
    "/report-org/{report_id}", tags=["zeno"], dependencies=[Depends(util.auth)]
)
async def delete_report_org(
    report_id: int, organization: Organization, request: Request
):
    """Remove an organizations from a report.

    Args:
        report_id (int): id dof the report to remove an organization from.
        organization (Organization): organization to be removed from the report.
        request (Request): http request to get user information from.
    """
    await util.report_editor(report_id, request)
    await delete.report_org(report_id, organization)
