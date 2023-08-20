"""Functions to upload data to Zeno's backend."""
import os
from enum import Enum
from functools import wraps
from pathlib import Path
from typing import Any, Callable

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
    env_path = Path("../frontend/.env")
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
                "name": project_name,
                "calculate_histogram_metrics": True,
                "num_items": 10,
                "editor": True,
                "public": False,
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
    def upload_datapoint(self, file_path: Path, datapoint_name: str):
        """Add a datapoint to an existing project.

        Requires a file where the data is saved.
        Has to be in the right format for the project's view.

        Args:
            file_path (Path): path to the data file to be added
            datapoint_name (str): name of the data point with extension.
        """
        self.user.check_token()
        with open(file_path, "rb") as file:
            requests.post(
                f'{os.environ["PUBLIC_BACKEND_ENDPOINT"]}/api/item/{self.project_uuid}',
                params={"name": datapoint_name},
                files={"file": file},
                headers={"Authorization": "Bearer " + str(self.user.access_token)},
            )

    @check_token
    def add_label(self, datapoint_name: str, label: str):
        """Add a label to a data point in the backend.

        Args:
            datapoint_name (str): name of the datapoint to add a label for.
            label (str): label to add to the datapoint.
        """
        self.user.check_token()
        requests.post(
            f'{os.environ["PUBLIC_BACKEND_ENDPOINT"]}/api/label/{self.project_uuid}',
            json={"item": datapoint_name, "label": label},
            headers={"Authorization": "Bearer " + str(self.user.access_token)},
        )

    @check_token
    def add_output(
        self,
        datapoint_name: str,
        model: str,
        output: Any,
    ):
        """Add an output value to a data point in the backend.

        Args:
            datapoint_name (str): name of the datapoint to add an output value for.
            model (str): the model for which to add an output value.
            output (Any): the output value to be added.
        """
        self.user.check_token()
        requests.post(
            f'{os.environ["PUBLIC_BACKEND_ENDPOINT"]}/api/output/{self.project_uuid}',
            json={
                "item": datapoint_name,
                "model": model,
                "output": output,
            },
            headers={"Authorization": "Bearer " + str(self.user.access_token)},
        )

    @check_token
    def add_predistill(
        self,
        datapoint_name: str,
        col_name: str,
        value: Any,
        type: MetadataType,
    ):
        """Add a predistill value to a data point in the backend.

        Args:
            datapoint_name (str): name of the datapoint to add a predistill value for.
            col_name (str): the name of the predistill column to add.
            value (Any): the value of the predistill column to add.
            type (MetadataType): the type of the predistill column.
        """
        self.user.check_token()
        requests.post(
            f'{os.environ["PUBLIC_BACKEND_ENDPOINT"]}/api/predistill/{self.project_uuid}',
            json={
                "item": datapoint_name,
                "col_name": col_name,
                "value": value,
                "type": type,
            },
            headers={"Authorization": "Bearer " + str(self.user.access_token)},
        )

    @check_token
    def add_postdistill(
        self,
        datapoint_name: str,
        col_name: str,
        model: str,
        value: Any,
        type: MetadataType,
    ):
        """Add a model-dependent postdistill value to a data point in the backend.

        Args:
            datapoint_name (str): name of the datapoint to add a postdistill value for.
            col_name (str): the name of the postdistill column to add.
            model (str): the model for which this value was calculated.
            value (Any): the value of the postdistill column to add.
            type (MetadataType): the type of the postdistill column.
        """
        self.user.check_token()
        requests.post(
            f'{os.environ["PUBLIC_BACKEND_ENDPOINT"]}/api/postdistill/{self.project_uuid}',
            json={
                "item": datapoint_name,
                "col_name": col_name,
                "value": value,
                "type": type,
                "model": model,
            },
            headers={"Authorization": "Bearer " + str(self.user.access_token)},
        )
