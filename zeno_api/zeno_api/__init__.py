"""Functions to upload data to Zeno's backend."""
import os
from enum import Enum
from functools import wraps
from pathlib import Path
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
    """Enumeration of possible metadata types in Zeno."""

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


def check_project(func: Callable):
    """Decorator to check whether the project_uuid is set.

    :meta private:

    Args:
        func (Callable): the function to be decorated.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        args[0].user.check_token()
        if args[0].project_uuid is not None:
            return func(*args, **kwargs)
        else:
            raise Exception(
                "Please create a project or set this object's project_uuid first."
            )

    return wrapper


class Zeno:
    """Provides upload functionality for zeno."""

    user: Cognito
    project_uuid: Optional[str]

    def __init__(self, user: Cognito) -> None:
        """Initialize the Zeno object for API upload calls.

        Args:
            user (Cognito): the user to issue the upload calls for.
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
        self.project_uuid = uuid.text[1:-1]

    @check_project
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

    @check_project
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

    @check_project
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

    @check_project
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

    @check_project
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
