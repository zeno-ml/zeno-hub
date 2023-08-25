"""Provides utility functions and classes for Zeno's Metrics."""
from enum import Enum
from typing import Any

import psycopg
from psycopg import sql
from pydantic import BaseModel, ConfigDict


def to_camel(string: str) -> str:
    """Converter for variables from snake_case to camelCase.

    Args:
        string (str): the variable to convert to camelCase.

    Returns:
        str: camelCase representation of the variable.
    """
    components = string.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class CamelModel(BaseModel):
    """Converting snake_case pydantic models to camelCase models."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class MetricType(Enum):
    """Enumeration of chart types available in Zeno.

    Attributes:
        ACCURACY: Metric calculating system accuracy.
    """

    ACCURACY = "ACCURACY"


class Metric:
    """Parent class for metrics in Zeno.

    Attributes:
        name (str): the name of the metric as displayed to the user.
    """

    name: str
    type: MetricType


class MetricReturn(CamelModel):
    """Return type of Zeno Metrics including the metric value and the sample size.

    Attributes:
        metric (float | None): the result value of the metric calculation.
        size (int): the sample size on which the metric was calculated.
    """

    metric: float | None
    size: int


def column_id_from_name_and_model(
    db_cursor: psycopg.Cursor[tuple[Any, ...]],
    project: str,
    column_name: str,
    model: str,
) -> str:
    """Get a column's id given its name and model.

    Args:
        db_cursor (psycopg.Cursor): the curser to execute DB queries.
        project (str): the project the user is currently working with.
        column_name (str): the name of the column to be fetched.
        model (str): the model of the column to be fetched.

    Returns:
        str: _description_
    """
    query = (
        sql.SQL(
            "SELECT column_id FROM {} "
            "WHERE name = %s AND (model = %s OR model IS NULL);"
        ).format(sql.Identifier(f"{project}_column_map")),
    )
    db_cursor.execute(query, [column_name, model])
    column_result = db_cursor.fetchone()
    return str(column_result[0]) if column_result is not None else ""
