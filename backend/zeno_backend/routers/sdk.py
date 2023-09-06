"""FastAPI server endpoints for the Zeno SDK."""
import io
import uuid

import pandas as pd
from amplitude import Amplitude, BaseEvent
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

client = Amplitude("9e6755badfe6f970b509d3325a6a6678")


class APIKeyBearer(HTTPBearer):
    """API key bearer authentication scheme."""

    def __init__(self, auto_error: bool = True):
        """Initialize the APIKeyBearer class.

        Args:
            auto_error (bool, optional): automatically report errors.
                Defaults to True.
        """
        super(APIKeyBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """Verify that the API key is valid.

        Args:
            request (Request): request object.
        """
        credentials: HTTPAuthorizationCredentials | None = await super(
            APIKeyBearer, self
        ).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
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
    """Create a new project.

    Args:
        project (Project): Project object.
        api_key (str, optional): API key.
    """
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

    client.track(
        BaseEvent(
            event_type="project_created",
            user_id=str(user_id + 10000),
            event_properties={"project": project.name},
        )
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
    """Upload a dataset to a Zeno project.

    Args:
        project (str): the UUID of the project to add data to.
        id_column (str): the name of the column containing the instance IDs.
        label_column (str | None, optional): the name of the column containing the
            instance labels. Defaults to None.
        data_column (str | None, optional): the name of the column containing the
            raw data. Only works for small text data. Defaults to None.
        file (UploadFile): the dataset to upload.
    """
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
    """Upload a system to a Zeno project.

    Args:
        project (str): the UUID of the project to add data to.
        system_name (str): the name of the system to upload.
        output_column (str): the name of the column containing the system output.
        id_column (str): the name of the column containing the instance IDs.
        file (UploadFile): the dataset to upload.
    """
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

    client.track(
        BaseEvent(
            event_type="system_uploaded",
            user_id="10000",
            event_properties={"project": project},
        )
    )
