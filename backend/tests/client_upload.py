"""Test the client upload functionality."""
import os

import pandas as pd
from zeno_client import ZenoClient, ZenoMetric


def test_upload_project():
    """Test the upload of a project."""
    api_key = os.environ.get("HUB_API_KEY")
    assert api_key is not None
    client = ZenoClient(api_key, endpoint="http://localhost:8000")
    assert client is not None
    project = client.create_project(
        name="My Project",
        view="text-classification",
        description="My first project",
        metrics=[ZenoMetric(name="accuracy", type="mean", columns=["accuracy"])],
    )
    df_dataset = pd.DataFrame(
        {
            "text": ["This is a test", "This is another test"],
            "label": ["test", "test"],
        }
    )
    df_dataset["id"] = df_dataset.index

    project.upload_dataset(
        df_dataset, id_column="id", label_column="label", data_column="text"
    )

    df_output = pd.DataFrame(
        {
            "output": ["test", "test"],
            "accuracy": [0.5, 0.5],
        }
    )
    df_output["id"] = df_output.index

    project.upload_system(
        df_output, name="my model", id_column="id", output_column="output"
    )
