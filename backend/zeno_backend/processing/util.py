"""Utility functions for the zeno backend."""

import pandas as pd

from zeno_backend.classes.base import MetadataType, ZenoColumn
from zeno_backend.processing.filtering import column_id_from_name_and_model

CHUNK_SIZE = 1024 * 1024  # adjust the chunk size as desired


def generate_diff_cols(
    df: pd.DataFrame, diff_col_1: ZenoColumn, diff_col_2: ZenoColumn, project: str
) -> pd.DataFrame:
    """Generate new difference column based on the dataframe and specified columns.

    Args:
        df (DataFrame): original dataframe.
        diff_col_1 (ZenoColumn): first column used to calculate the difference.
        diff_col_2 (ZenoColumn): second column used to calculate the difference.
        project (str): project id for which to get the diff column.

    Returns:
        DataFrame: new dataframe containing the diff column.
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
