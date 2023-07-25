"""Utility functions for the zeno backend."""
from pathlib import Path

import aiofiles
import pandas as pd
from fastapi import File, HTTPException, UploadFile, status

from zeno_backend.classes.base import MetadataType, ZenoColumn
from zeno_backend.database.select import column_id_from_name_and_model

CHUNK_SIZE = 1024 * 1024  # adjust the chunk size as desired


def generate_diff_cols(
    df: pd.DataFrame, diff_col_1: ZenoColumn, diff_col_2: ZenoColumn, project: str
) -> pd.DataFrame:
    """Generate new difference column based on the dataframe and specified columns.

    Args:
        df (DataFrame): The original dataframe.
        diff_col_1 (ZenoColumn): The first column used to calculate the difference.
        diff_col_2 (ZenoColumn): The second column used to calculate the difference.
        project (str): The project id for which to get the diff column.

    Returns:
        DataFrame: Return the new dataframe containing the diff column.
    """
    if (
        diff_col_1.column_type != diff_col_2.column_type
        or diff_col_1.data_type != diff_col_2.data_type
    ):
        return df

    if diff_col_1.model is None or diff_col_2.model is None:
        return df

    col1_id = column_id_from_name_and_model(
        project=project, column_name=diff_col_1.name, model=diff_col_1.model
    )
    col2_id = column_id_from_name_and_model(
        project=project, column_name=diff_col_2.name, model=diff_col_2.model
    )

    # various metadata type difference
    if diff_col_1.data_type == MetadataType.CONTINUOUS:
        df.loc[:, "diff"] = df[col1_id] - df[col2_id]
    else:
        df.loc[:, "diff"] = df[col1_id] != df[col2_id]
    return df


async def save_file(file_path: Path, file: UploadFile = File(...)):
    """Save a file to a specified path.

    Args:
        file_path (Path): destination to write the file to.
        file (UploadFile, optional): file to write to disk. Defaults to File(...).

    Raises:
        HTTPException: file could not be saved.
    """
    try:
        async with aiofiles.open(file_path, "wb") as out_file:
            while chunk := await file.read(CHUNK_SIZE):
                await out_file.write(chunk)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="There was an error uploading the file",
        ) from exc
    finally:
        await file.close()
