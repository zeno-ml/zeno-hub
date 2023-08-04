"""Functions to upload data to Zeno's backend."""
import os
import uuid

import requests


def create_project(project_name: str, view: str = "image-classification"):
    """Creates an empty project in Zeno's backend.

    Args:
        project_name (str): the name of the project to be created.
        view (str, optional): the view that the project uses to display data.
        Defaults to "image-classification".
    """
    requests.post(
        f'{os.environ["PUBLIC_BACKEND_ENDPOINT"]}/api/project',
        json={
            "uuid": str(uuid.uuid4()),
            "view": view,
            "name": project_name,
            "calculate_histogram_metrics": True,
            "num_items": 10,
            "editor": True,
            "public": False,
        },
        headers={"Authorization": "Bearer " + os.environ["ZENO_ACCESS_TOKEN"]},
    )
