"""FastAPI server endpoints for the Zeno SDK."""
import io
import uuid

import pandas as pd
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from zeno_backend.classes.project import Project
from zeno_backend.database import insert, select


class APIKeyBearer(HTTPBearer):
    """API key bearer authentication scheme."""

    def __init__(self, auto_error: bool = True):
        """Initialize the APIKeyBearer class.

        Args:
            auto_error (bool, optional): Automatically report errors.
                Defaults to True.
        """
        super(APIKeyBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """Verify that the API key is valid.

        Args:
            request (Request): Request object.
        """
        credentials: HTTPAuthorizationCredentials | None = await super(
            APIKeyBearer, self
        ).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )

            print(credentials.credentials)
            if not self.verify_api_key(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_api_key(self, api_key: str) -> bool:
        """Verify that the API key is valid.

        Args:
            api_key (str): API key to verify.


        Returns:
            bool: True if the API key is valid, False otherwise.
        """
        api_key_is_valid = select.api_key_exists(api_key)
        return api_key_is_valid


router = APIRouter(tags=["zeno"], dependencies=[Depends(APIKeyBearer())])


@router.post("/project")
def create_project(project: Project, api_key=Depends(APIKeyBearer())):
    user_id = select.user_id_by_api_key(api_key)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=("ERROR: Invalid API key."),
        )

    if select.project_exists(user_id, project.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=("ERROR: Project already exists."),
        )

    project.uuid = str(uuid.uuid4())
    insert.project(project, user_id)
    return project.uuid


@router.post("/dataset/{project}")
def upload_dataset(
    project: str,
    id_column: str = Form(...),
    label_column: str = Form(None),
    data_column: str = Form(None),
    file: UploadFile = File(...),
):
    try:
        bytes = file.file.read()
        dataset_df = pd.read_feather(io.BytesIO(bytes))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=("ERROR: Unable to read dataset: " + str(e)),
        ) from e

    try:
        insert.dataset(project, dataset_df, id_column, label_column, data_column)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=("ERROR: Unable to create dataset table: " + str(e)),
        ) from e


@router.post("/system/{project}")
def upload_system(
    project: str,
    system_name: str = Form(...),
    output_column: str = Form(...),
    id_column: str = Form(...),
    file: UploadFile = File(...),
):
    try:
        bytes = file.file.read()
        system_df = pd.read_feather(io.BytesIO(bytes))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=("ERROR: Unable to read system data: " + str(e)),
        ) from e

    try:
        insert.system(project, system_df, system_name, output_column, id_column)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=("ERROR: Unable to create system table: " + str(e)),
        ) from e
