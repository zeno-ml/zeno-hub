"""FastAPI server endpoints for tag-related queries."""
from amplitude import BaseEvent
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
)

import zeno_backend.database.delete as delete
import zeno_backend.database.insert as insert
import zeno_backend.database.select as select
import zeno_backend.database.update as update
import zeno_backend.util as util
from zeno_backend.classes.amplitude import AmplitudeHandler
from zeno_backend.classes.tag import Tag

router = APIRouter(tags=["zeno"])


@router.get(
    "/tags/{project_uuid}",
    response_model=list[Tag],
    tags=["zeno"],
)
def get_tags(project_uuid: str, request: Request):
    """Get all tags for a project.

    Args:
        project_uuid (str): UUID of the project to get all tags for.
        request (Request): http request to get user information from.

    Returns:
        list[Tag]: list of all of a project's tags.
    """
    util.project_access_valid(project_uuid, request)
    return select.tags(project_uuid)


@router.post(
    "/tags-for-projects/",
    response_model=list[Tag],
    tags=["zeno"],
)
def get_tags_for_projects(project_uuids: list[str]):
    """Get all tags for a list of projects.

    Args:
        project_uuids (list[str]): UUIDs of all projects to get tags for.

    Returns:
        list[Tag]: all tags for the specified projects.
    """
    return select.tags_for_projects(project_uuids)


@router.post(
    "/tag/{project_uuid}",
    response_model=int,
    tags=["zeno"],
)
def add_tag(tag: Tag, project_uuid: str, current_user=Depends(util.auth.claim())):
    """Add a tag to a project.

    Args:
        tag (Tag): the tag to be added.
        project_uuid (str): UUID of the project to add the tag to.
        current_user (Any, optional): user adding the new tag.
            Defaults to Depends(util.auth.claim()).

    Raises:
        HTTPException: error if adding the tag failed.

    Returns:
        int: id of the newly created tag.
    """
    id = insert.tag(project_uuid, tag)
    if id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to insert tag",
        )
    AmplitudeHandler().track(
        BaseEvent(
            event_type="Tag Created",
            user_id=current_user["sub"],
            event_properties={"project_uuid": project_uuid},
        )
    )
    return id


@router.patch("/tag/{project_uuid}", tags=["zeno"], dependencies=[Depends(util.auth)])
def update_tag(tag: Tag, project_uuid: str):
    """Update a tag in the database.

    Args:
        tag (Tag): updated tag.
        project_uuid (str): project to which the tag belongs.
    """
    update.tag(tag, project_uuid)


@router.delete("/tag", tags=["zeno"], dependencies=[Depends(util.auth)])
def delete_tag(tag: Tag):
    """Delete a tag from the database.

    Args:
        tag (Tag): tag to be deleted from the database.
    """
    delete.tag(tag)
