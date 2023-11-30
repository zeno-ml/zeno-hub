"""FastAPI server endpoints for folder-related queries."""

from fastapi import APIRouter, Depends, HTTPException, Request, status

import zeno_backend.database.delete as delete
import zeno_backend.database.insert as insert
import zeno_backend.database.select as select
import zeno_backend.database.update as update
import zeno_backend.util as util
from zeno_backend.classes.folder import Folder

router = APIRouter(tags=["zeno"])


@router.get(
    "/folders/{project}",
    response_model=list[Folder],
    tags=["zeno"],
)
def get_folders(project: str, request: Request):
    """Get all folders for a specific project.

    Args:
        project (str): project to get all folders for.
        request (Request): http request to get user information from.

    Returns:
        list[Folder]: all folders for a specific project.
    """
    util.project_access_valid(project, request)
    return select.folders(project)


@router.post(
    "/folder/{project}",
    response_model=int,
    tags=["zeno"],
    dependencies=[Depends(util.auth)],
)
def add_folder(project: str, name: str, request: Request):
    """Add a folder to a project.

    Args:
        project (str): project to add the folder to.
        name (str): name of the folder to be added.
        request (Request): http request to get user information from.

    Raises:
        HTTPException: error if folder cannot be added.

    Returns:
        int: id of the newly created folder.
    """
    util.project_editor(project, request)
    id = insert.folder(project, name)
    if id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to insert folder",
        )
    return id


@router.patch("/folder/{project}", tags=["zeno"], dependencies=[Depends(util.auth)])
def update_folder(folder: Folder, project: str, request: Request):
    """Updatae a folder in the database.

    Args:
        folder (Folder): new folder specification.
        project (str): project that the folder belongs to.
        request (Request): http request to get user information from.
    """
    util.project_editor(project, request)
    update.folder(folder, project)


@router.delete("/folder", tags=["zeno"], dependencies=[Depends(util.auth)])
async def delete_folder(folder: Folder, request: Request, delete_slices: bool = False):
    """Delete an existing folder from the database.

    Args:
        folder (Folder): folder to be deleted.
        request (Request): http request to get user information from.
        delete_slices (bool, optional): Whether to also delete all slices in the folder.
            Defaults to False.
    """
    util.project_editor(folder.project, request)
    await delete.folder(folder, delete_slices)
