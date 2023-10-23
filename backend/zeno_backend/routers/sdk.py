"""FastAPI server endpoints for the Zeno SDK."""
import uuid

import pyarrow as pa
from amplitude import BaseEvent
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    Response,
    UploadFile,
    status,
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from zeno_backend.classes.amplitude import AmplitudeHandler
from zeno_backend.classes.project import Project
from zeno_backend.database import delete, insert, select, update

# MUST reflect views in frontend/src/lib/components/instance-views/views/viewMap.ts
VIEWS = [
    "audio-transcription",
    "chatbot",
    "code-generation",
    "image-classification",
    "image-segmentation",
    "openai-chat-markdown",
    "openai-chat",
    "space-separated-values",
    "text-classification",
    "rag",
]

# Bump only for breaking changes
MIN_CLIENT_VERSION = "0.1.9"


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
                    status_code=403,
                    detail=(
                        "ERROR: Invalid API key. Double check your API key or generate"
                        + " a new one at https://hub.zenoml.com/account."
                    ),
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403,
                detail=(
                    "ERROR: Invalid API key. Double check your API key or generate"
                    + " a new one at https://hub.zenoml.com/account."
                ),
            )

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


@router.post("/project", status_code=200, response_model=Project)
def create_project(
    project: Project, response: Response, api_key=Depends(APIKeyBearer())
):
    """Create a new project.

    Args:
        project (Project): Project object.
        response (Response): response object.
        api_key (str, optional): API key.
    """
    user = select.user_by_api_key(api_key)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                "ERROR: Invalid API key. Double check your API key or generate"
                + " a new one at https://hub.zenoml.com/account."
            ),
        )

    if project.view not in VIEWS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "ERROR: Invalid view. Please reference https://zenoml.com/docs/views/"
                + " for a list of valid views."
            ),
        )

    if user is not None and select.project_exists(user.id, project.name):
        project_uuid = select.project_uuid(user.name, project.name)
        if project_uuid is not None:
            project.uuid = project_uuid
            update.project(project)
            update.project_metrics(project)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=("ERROR: Project already exists but could not be updated."),
            )
    else:
        project.uuid = str(uuid.uuid4())
        insert.project(project, user.id)
        AmplitudeHandler().track(
            BaseEvent(
                event_type="Project Created",
                user_id=user.cognito_id,
                event_properties={"project_uuid": project.uuid},
            )
        )
        response.status_code = status.HTTP_201_CREATED
    project.owner_name = user.name
    return project


@router.post("/dataset-schema")
async def upload_dataset_schema(
    project_uuid=Form(...),
    id_column=Form(...),
    data_column=Form(...),
    label_column=Form(None),
    file: UploadFile = File(...),
    api_key=Depends(APIKeyBearer()),
):
    """Upload a dataset schema to the database. Called before uploading data.

    Args:
        project_uuid (str): the UUID of the project to add data to.
        id_column (str): the name of the column containing the ID.
        data_column (str): the name of the column containing the data.
        label_column (str): the name of the column containing the label.
        file (DatasetSchema): the dataset schema to upload.
        api_key (str, optional): API key.
    """
    user = select.user_by_api_key(api_key)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                "ERROR: Invalid API key. Double check your API key or generate"
                + " a new one at https://hub.zenoml.com/account."
            ),
        )
    if not select.project_uuid_exists(project_uuid):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=("ERROR: Project does not exist."),
        )

    contents = await file.read()
    schema = pa.ipc.read_schema(pa.py_buffer(contents))

    res = await insert.dataset_schema(
        project_uuid, id_column, data_column, label_column, schema
    )

    AmplitudeHandler().track(
        BaseEvent(
            event_type="Dataset Uploaded",
            user_id=user.cognito_id,
            event_properties={"project_uuid": project_uuid},
        )
    )

    return res


@router.post("/dataset/{project_uuid}")
async def upload_dataset(
    project_uuid: str,
    file: UploadFile = File(...),
    api_key=Depends(APIKeyBearer()),
):
    """Upload a dataset to a Zeno project.

    Args:
        project_uuid (str): the UUID of the project to add data to.
        file (UploadFile): the dataset to upload. Serialized Arrow RecordBatch.
        api_key (str, optional): API key.
    """
    user = select.user_by_api_key(api_key)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                "ERROR: Invalid API key. Double check your API key or generate"
                + " a new one at https://hub.zenoml.com/account."
            ),
        )
    if not select.project_uuid_exists(project_uuid):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=("ERROR: Project does not exist."),
        )

    contents = await file.read()
    reader = pa.ipc.RecordBatchFileReader(contents)
    batch = reader.get_batch(0)

    try:
        await insert.dataset(project_uuid, batch)
    except Exception as e:
        # If one of the batches fails, delete the entire dataset.
        await delete.dataset(project_uuid)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=("ERROR: Unable to create dataset table." + str(e)),
        )


@router.post("/system-schema")
async def upload_system_schema(
    project_uuid=Form(...),
    system_name=Form(...),
    id_column=Form(...),
    output_column=Form(...),
    file: UploadFile = File(...),
    api_key=Depends(APIKeyBearer()),
):
    """Upload a dataset schema to the database. Called before uploading system.

    Args:
        project_uuid (str): the UUID of the project to add data to.
        system_name (str): the name of the system.
        id_column (str): the name of the column containing the ID.
        output_column (str): the name of the column containing the output.
        file (Schema): the system PyArrow schema to upload.
        api_key (str, optional): API key.
    """
    user = select.user_by_api_key(api_key)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                "ERROR: Invalid API key. Double check your API key or generate"
                + " a new one at https://hub.zenoml.com/account."
            ),
        )
    if not select.project_uuid_exists(project_uuid):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=("ERROR: Project does not exist."),
        )

    contents = await file.read()
    schema = pa.ipc.read_schema(pa.py_buffer(contents))

    res = await insert.system_schema(
        project_uuid, system_name, id_column, output_column, schema
    )

    AmplitudeHandler().track(
        BaseEvent(
            event_type="System Uploaded",
            user_id=user.cognito_id,
            event_properties={"project_uuid": project_uuid},
        )
    )

    return res


@router.post("/system/{project_uuid}/{system_name}")
async def upload_system(
    project_uuid: str,
    system_name: str,
    file: UploadFile = File(...),
    api_key=Depends(APIKeyBearer()),
):
    """Upload a system to a Zeno project.

    Args:
        project_uuid (str): the UUID of the project to add the system to.
        system_name (str): the name of the system.
        file (UploadFile): the system to upload. Serialized Arrow RecordBatch.
        api_key (str, optional): API key.
    """
    user = select.user_by_api_key(api_key)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                "ERROR: Invalid API key. Double check your API key or generate"
                + " a new one at https://hub.zenoml.com/account."
            ),
        )
    if not select.project_uuid_exists(project_uuid):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=("ERROR: Project does not exist."),
        )

    contents = await file.read()
    reader = pa.ipc.RecordBatchFileReader(contents)
    batch = reader.get_batch(0)

    try:
        await insert.system(project_uuid, batch)
    except Exception as e:
        # If one of the batches fails, delete the entire system.
        await delete.system(project_uuid, system_name)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=("ERROR: Unable to upload system: " + str(e)),
        )


@router.delete("/system/{project_uuid}/{system_name}")
async def delete_system(project_uuid: str, system_name: str):
    """Delete a system from a Zeno project.

    Args:
        project_uuid (str): the UUID of the project to delete the system from.
        system_name (str): the name of the system.
    """
    await delete.system(project_uuid, system_name)


@router.get("/min-client-version")
def min_client_version():
    """Get the minimum client version required to use the server."""
    return MIN_CLIENT_VERSION
