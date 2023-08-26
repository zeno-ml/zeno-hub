"""Utility functions for database operations."""
import hashlib

import pandas as pd

from zeno_backend.classes.base import MetadataType


def resolve_metadata_type(data_frame: pd.DataFrame, column: str) -> MetadataType:
    """Get the MetadataType of a dataframe column.

    Args:
        data_frame (pd.DataFrame): dataframe that contains the column.
        column (str): column for which to determine the type.

    Returns:
        MetadataType: MetadataType of the dataframe column.
    """
    dtype = data_frame[column].dtype
    if pd.api.types.is_any_real_numeric_dtype(dtype):
        return MetadataType.CONTINUOUS
    elif pd.api.types.is_bool_dtype(dtype):
        return MetadataType.BOOLEAN
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return MetadataType.DATETIME
    elif pd.api.types.is_string_dtype(dtype):
        return MetadataType.NOMINAL
    return MetadataType.OTHER


def hash_api_key(api_key: str) -> str:
    """Hash an API key.

    Args:
        api_key (str): API key to hash.

    Returns:
        str: Hashed API key.
    """
    hasher = hashlib.sha256()

    hasher.update(api_key.encode("utf-8"))

    return hasher.hexdigest()
