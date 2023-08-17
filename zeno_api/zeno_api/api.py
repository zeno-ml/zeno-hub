"""Functions to upload data to Zeno's backend."""
import os
from enum import Enum
from pathlib import Path
from typing import Any

import requests
from pycognito import Cognito


class MetadataType(str, Enum):
    """Enumeration of possible metadata types in Zeno."""

    NOMINAL = "NOMINAL"
    CONTINUOUS = "CONTINUOUS"
    BOOLEAN = "BOOLEAN"
    DATETIME = "DATETIME"
    OTHER = "OTHER"


def create_project(
    project_name: str, user: Cognito, view: str = "image-classification"
) -> str:
    """Creates an empty project in Zeno's backend.

    The returned uuid has to be used to upload data.

    Args:
        project_name (str): the name of the project to be created.
        user (Cognito): the cognito user to authenticate the upload.
        view (str, optional): the view that the project uses to display data.
        Defaults to "image-classification".

    Returns:
        str: uuid of the newly created project.
    """
    user.check_token()
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
        headers={"Authorization": "Bearer " + str(user.access_token)},
    )
    return uuid.text[1:-1]


def upload_datapoint(
    project_uuid: str, file_path: Path, datapoint_name: str, user: Cognito
):
    """Add a datapoint to an existing project.

    Requires a file where the data is saved.
    Has to be in the right format for the project's view.

    Args:
        project_uuid (str): id of the project for which to add data.
        file_path (Path): path to the data file to be added
        datapoint_name (str): name of the data point with extension.
        user (Cognito): the cognito user to authenticate the upload.
    """
    user.check_token()
    with open(file_path, "rb") as file:
        requests.post(
            f'{os.environ["PUBLIC_BACKEND_ENDPOINT"]}/api/item/{project_uuid}',
            params={"name": datapoint_name},
            files={"file": file},
            headers={"Authorization": "Bearer " + str(user.access_token)},
        )


def add_label(project_uuid: str, datapoint_name: str, label: str, user: Cognito):
    """Add a label to a data point in the backend.

    Args:
        project_uuid (str): project for which to modify data.
        datapoint_name (str): name of the datapoint to add a label for.
        label (str): label to add to the datapoint.
        user (Cognito): the cognito user to authenticate the upload.
    """
    user.check_token()
    requests.post(
        f'{os.environ["PUBLIC_BACKEND_ENDPOINT"]}/api/label/{project_uuid}',
        json={"item": datapoint_name, "label": label},
        headers={"Authorization": "Bearer " + str(user.access_token)},
    )


def add_output(
    project_uuid: str, datapoint_name: str, model: str, output: Any, user: Cognito
):
    """Add an output value to a data point in the backend.

    Args:
        project_uuid (str): project for which to modify data.
        datapoint_name (str): name of the datapoint to add an output value for.
        model (str): the model for which to add an output value.
        output (Any): the output value to be added.
        user (Cognito): the cognito user to authenticate the upload.
    """
    user.check_token()
    requests.post(
        f'{os.environ["PUBLIC_BACKEND_ENDPOINT"]}/api/output/{project_uuid}',
        json={
            "item": datapoint_name,
            "model": model,
            "output": output,
        },
        headers={"Authorization": "Bearer " + str(user.access_token)},
    )


def add_predistill(
    project_uuid: str,
    datapoint_name: str,
    col_name: str,
    value: Any,
    type: MetadataType,
    user: Cognito,
):
    """Add a predistill value to a data point in the backend.

    Args:
        project_uuid (str): project for which to modify data.
        datapoint_name (str): name of the datapoint to add a predistill value for.
        col_name (str): the name of the predistill column to add.
        value (Any): the value of the predistill column to add.
        type (MetadataType): the type of the predistill column.
        user (Cognito): the cognito user to authenticate the upload.
    """
    user.check_token()
    requests.post(
        f'{os.environ["PUBLIC_BACKEND_ENDPOINT"]}/api/predistill/{project_uuid}',
        json={
            "item": datapoint_name,
            "col_name": col_name,
            "value": value,
            "type": type,
        },
        headers={"Authorization": "Bearer " + str(user.access_token)},
    )


def add_postdistill(
    project_uuid: str,
    datapoint_name: str,
    col_name: str,
    model: str,
    value: Any,
    type: MetadataType,
    user: Cognito,
):
    """Add a model-dependent postdistill value to a data point in the backend.

    Args:
        project_uuid (str): project for which to modify data.
        datapoint_name (str): name of the datapoint to add a postdistill value for.
        col_name (str): the name of the postdistill column to add.
        model (str): the model for which this value was calculated.
        value (Any): the value of the postdistill column to add.
        type (MetadataType): the type of the postdistill column.
        user (Cognito): the cognito user to authenticate the upload.
    """
    user.check_token()
    requests.post(
        f'{os.environ["PUBLIC_BACKEND_ENDPOINT"]}/api/postdistill/{project_uuid}',
        json={
            "item": datapoint_name,
            "col_name": col_name,
            "value": value,
            "type": type,
            "model": model,
        },
        headers={"Authorization": "Bearer " + str(user.access_token)},
    )
