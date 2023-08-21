"""Uploading existing zeno project to a zeno backend using the Zeno API.

We assume that this existing project has been created with an older version of zeno.
Therefore, this script makes assumptions about the column names and data structure of
the CSV.
"""
import argparse
import ast
import json
from pathlib import Path

import pandas as pd
from pandas.api.types import (
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_string_dtype,
)

import zeno_api
from zeno_api import MetadataType

parser = argparse.ArgumentParser(
    prog="Upload Zeno project data.",
    description="Uploads data for a Zeno project that has been saved as a csv.",
)
parser.add_argument("--csv_path", required=True)
parser.add_argument("--connex_username", required=True)
parser.add_argument("--connex_password", required=True)
parser.add_argument("--view", required=True)
parser.add_argument("--project_name", required=True)
args = parser.parse_args()


def resolve_column_type(df: pd.DataFrame, col: str) -> MetadataType:
    """Get the Zeno MetadataType of a pandas dataframe column.

    Args:
        df (pd.DataFrame): dataframe for which to get the column type.
        col (str): name of the column for which to get the type.

    Returns:
        MetadataType: the metadata type of the column.
    """
    if is_bool_dtype(df[col]):
        return MetadataType.BOOLEAN
    if is_datetime64_any_dtype(df[col]):
        return MetadataType.DATETIME
    if is_string_dtype(df[col]):
        return MetadataType.NOMINAL
    if is_numeric_dtype(df[col]):
        return MetadataType.CONTINUOUS
    return MetadataType.OTHER


zeno = zeno_api.authenticate(args.connex_username, args.connex_password)
project = zeno.create_project(args.project_name, view=args.view)

data_frame = pd.read_csv(args.csv_path)
data_frame = data_frame.fillna("")
output_cols = list(
    filter(lambda col: str(col).startswith("OUTPUToutput"), data_frame.columns)
)
models = list(
    set(list(map(lambda col: str(col).replace("OUTPUToutput", ""), output_cols)))
)
predistill_cols = list(
    filter(lambda col: str(col).startswith("PREDISTILL"), data_frame.columns)
)
postdistill_cols = list(
    filter(lambda col: str(col).startswith("POSTDISTILL"), data_frame.columns)
)

file_path = Path("data.json")
for index, row in data_frame.iterrows():
    with open(file_path, "w") as f:
        messages_obj = ast.literal_eval(row["messages"])
        json.dump(messages_obj, f)
    datapoint_name = f"{index}.json"
    project.upload_datapoint(file_path, datapoint_name)
    project.add_label(datapoint_name, row["label"])
    for col in output_cols:
        model_name = str(col).replace("OUTPUToutput", "")
        project.add_output(datapoint_name, model_name, row[str(col)])
    for col in predistill_cols:
        col_name = str(col).replace("PREDISTILL", "")
        type = resolve_column_type(data_frame, str(col))
        project.add_feature(datapoint_name, col_name, row[str(col)], type)
    for col in postdistill_cols:
        col_name = str(col).replace("POSTDISTILL", "")
        type = resolve_column_type(data_frame, str(col))
        model = ""
        for m in models:
            if col_name.endswith(m):
                model = m
                col_name = col_name.replace(m, "", 1)
        project.add_feature(datapoint_name, col_name, row[str(col)], type, model)

file_path.unlink()
