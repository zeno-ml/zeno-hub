"""Functions to upload data to Zeno's backend."""
import os
from enum import Enum
from functools import wraps
from pathlib import Path, PurePath
from typing import Any, Callable, Optional

import requests
from dotenv import load_dotenv
from pycognito import Cognito


def authenticate(username: str, password: str):
    """Initializes the user object for all upload operations.

    Has to be called before starting to upload any data.

    Args:
        username (str): the username for which to get the access token.
        password (str): the password used by the user to login.


    Returns:
        Zeno: the zeno api objec to issue upload commands on.
    """
    # load env vars for cognito if available
    env_path = Path("../../frontend/.env")
    if env_path.exists():
        load_dotenv(env_path)

    # function to get the user from cognito
    user = Cognito(
        os.environ["ZENO_USER_POOL_ID"],
        os.environ["ZENO_USER_POOL_CLIENT_ID"],
        username=username,
    )
    user.authenticate(password=password)
    return Zeno(user)


class MetadataType(str, Enum):
    """Enumeration of possible metadata types in Zeno.

    Attributes:
        NOMINAL: Nominal metadata type, e.g. string or small cardinality number.
        CONTINUOUS: Continuous metadata type, e.g. large cardinality number.
        BOOLEAN: Boolean metadata type, e.g. True or False.
        DATETIME: Datetime metadata type, e.g. 2021-01-01 00:00:00.
        OTHER: Any other metadata type, e.g. strings.
    """

    NOMINAL = "NOMINAL"
    CONTINUOUS = "CONTINUOUS"
    BOOLEAN = "BOOLEAN"
    DATETIME = "DATETIME"
    OTHER = "OTHER"


def check_token(func: Callable):
    """Decorator to check whether the user token is valid.

    :meta private:

    Args:
        func (Callable): the function to be decorated.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        args[0].user.check_token()
        return func(*args, **kwargs)

    return wrapper


class Zeno:
    """Used to get or create projects for data uploads."""

    user: Cognito

    def __init__(self, user: Cognito) -> None:
        """Initialize the Zeno object for project management.

        Args:
            user (Cognito): the user to get the project for.
        """
        self.user = user

    @check_token
    def create_project(self, project_name: str, view: str = "image-classification"):
        """Creates an empty project in Zeno's backend.

        The returned uuid has to be used to upload data.

        Args:
            project_name (str): the name of the project to be created.
            view (str, optional): the view that the project uses to display data.
                Defaults to "image-classification".
        """
        uuid = requests.post(
            f'{os.environ["PUBLIC_BACKEND_ENDPOINT"]}/api/project',
            json={
                "uuid": "",
                "view": view,
                "dataUrl": None,
                "name": project_name,
                "editor": True,
                "public": False,
                "samplesPerPage": 10,
            },
            headers={"Authorization": "Bearer " + str(self.user.access_token)},
        )
        return Project(self.user, uuid.text[1:-1])

    def get_project(self, project_uuid: str):
        """Get a project object by its UUID.

        Args:
            project_uuid (str): the UUID of the project to be fetched.
        """
        return Project(self.user, project_uuid)


class Project:
    """Provides data upload functionality for a Zeno project."""

    user: Cognito
    project_uuid: str

    def __init__(self, user: Cognito, project_uuid: str) -> None:
        """Initialize the Project object for API upload calls.

        Args:
            user (Cognito): the user to authenticate uploads with.
            project_uuid (str): the ID of the project to add data to.
        """
        self.user = user
        self.project_uuid = project_uuid

    @check_token
    def add_datapoint(self, data_id: int | str, data: Optional[Path | str] = None):
        """Add a datapoint to an existing project.

        The data parameter can be left empty if a URL (URL part with base_url set for
        the project) is used for data_id. If data is left empty, you have to set data_id
        to a valid URL (URL part with base_url set for the project).

        Otherwise, the data parameter can be either a string containing the data
        directly or a Path to a file to be uploaded.
        If a file path is provided, it has to be in the right format for the project's
        view to be displayed.

        Args:
            data_id (int | str): the unique ID of the data point to be added.
            data (Optional[Path | str]): the path to the file containing the data.
                Defaults to None.
        """
        if isinstance(data, PurePath):
            with open(data, "rb") as file:
                requests.post(
                    f'{os.environ["PUBLIC_BACKEND_ENDPOINT"]}/api/upload_datapoint/{self.project_uuid}',
                    json={"dataId": data_id, "data": None},
                    files={"file": file},
                    headers={"Authorization": "Bearer " + str(self.user.access_token)},
                )
        else:
            requests.post(
                f'{os.environ["PUBLIC_BACKEND_ENDPOINT"]}/api/add_datapoint/{self.project_uuid}',
                json={"dataId": data_id, "data": data},
                headers={"Authorization": "Bearer " + str(self.user.access_token)},
            )

    @check_token
    def add_label(self, data_id: int | str, label: str):
        """Add a label to a data point in the backend.

        Args:
            data_id (int | str): name of the datapoint to add a label for.
            label (str): label to add to the datapoint.
        """
        requests.post(
            f'{os.environ["PUBLIC_BACKEND_ENDPOINT"]}/api/label/{self.project_uuid}',
            json={"data_id": data_id, "label": label},
            headers={"Authorization": "Bearer " + str(self.user.access_token)},
        )

    @check_token
    def add_output(
        self,
        data_id: int | str,
        output: Any,
        model: str,
    ):
        """Add an output value to a data point in the backend.

        Args:
            data_id (int | str): unique id of the datapoint to add an output value for.
            output (Any): the output value to be added.
            model (str): the model for which to add an output value.
        """
        requests.post(
            f'{os.environ["PUBLIC_BACKEND_ENDPOINT"]}/api/output/{self.project_uuid}',
            json={
                "data_id": data_id,
                "output": output,
                "model": model,
            },
            headers={"Authorization": "Bearer " + str(self.user.access_token)},
        )

    @check_token
    def add_feature(
        self,
        col_name: str,
        data_id: int | str,
        value: Any,
        type: MetadataType,
        model: Optional[str] = None,
    ):
        """Add a feature value to a data point in the backend.

        Args:
            data_id (int | str): name of the datapoint to add a feature value for.
            col_name (str): the name of the feature column to add.
            value (Any): the value of the feature column to add.
            type (MetadataType): the type of the feature column.
            model (Optional[str], optional): model that relates to the feature column.
                Defaults to None.
        """
        requests.post(
            f'{os.environ["PUBLIC_BACKEND_ENDPOINT"]}/api/feature/{self.project_uuid}',
            json={
                "col_name": col_name,
                "data_id": data_id,
                "value": value,
                "type": type.value,
                "model": model,
            },
            headers={"Authorization": "Bearer " + str(self.user.access_token)},
        )
