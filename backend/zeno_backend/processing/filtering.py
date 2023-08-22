"""Functions for parsing filter predicates and filtering data."""
from typing import List, Optional, Union

from psycopg import sql

from zeno_backend.classes.base import MetadataType, ZenoColumn
from zeno_backend.classes.filter import FilterPredicateGroup
from zeno_backend.classes.metadata import HistogramBucket
from zeno_backend.database.select import column_id_from_name_and_model


def filter_to_sql(
    filter: FilterPredicateGroup, project: str, model: Optional[str] = None
) -> sql.Composed:
    """Converting a filter representation to a SQL string for the database.

    Args:
        filter (FilterPredicateGroup): the filter to be converted to sql.
        project (str): the project the user is currently working with.
        model (Optional[str], optional): model for which to get a SQL filter.
        Defaults to None.

    Returns:
        sql.Composed: filter to be used in a SQL query.
    """
    filt = sql.Composed([])
    for f in filter.predicates:
        if isinstance(f, FilterPredicateGroup):
            if len(f.predicates) != 0:
                filt = (
                    filt
                    + sql.SQL(f.join.value)
                    + sql.SQL("(")
                    + filter_to_sql(f, project, model)
                    + sql.SQL(")")
                )
        else:
            try:
                val = str(float(f.value))
            except ValueError:
                if str(f.value).lower() in [
                    "true",
                    "false",
                ]:
                    val = "True" if str(f.value).lower() == "true" else "False"
                else:
                    val = f.value
            column_id = (
                f.column.id
                if model is None
                else column_id_from_name_and_model(project, f.column.name, model)
            )
            filt = (
                filt
                + sql.SQL(f.join.value)
                + sql.SQL("({} ").format(
                    sql.Identifier(column_id),
                )
                + sql.SQL(f.operation.literal())
                + sql.SQL(" {})").format(sql.Literal(val))
            )
    return filt


def table_filter(
    project: str,
    model: Optional[str],
    filter_predicates: Optional[FilterPredicateGroup] = None,
    data_ids: Optional[List[str]] = None,
) -> Optional[sql.Composed]:
    """Generate a filter string to filter the data table of a project.

    Args:
        project (str): the project the user is currently working with
        model (Optional[str]): the model for which to generate the filter.
        filter_predicates (Optional[FilterPredicateGroup], optional): The filter
        predicates to apply to the table. Default None.
        data_ids (Optional[List[str]], optional): a list of datapoints to limit the
            table output to. Default None.

    Returns:
        Optional[sql.Composed]: filter to filter a SQL table with.
    """
    filter_result: Union[sql.Composed, None] = None
    if filter_predicates is not None and len(filter_predicates.predicates) > 0:
        filter_result = filter_to_sql(filter_predicates, project, model)

    if data_ids is not None and len(data_ids) > 0:
        datapoint_filter = sql.SQL("data_id IN ({})").format(
            sql.SQL(",").join(map(sql.Literal, data_ids))
        )
        if filter_result is not None:
            filter_result += sql.SQL(" AND ") + datapoint_filter
        filter_result = datapoint_filter
    return filter_result


def bucket_filter(col: ZenoColumn, bucket: HistogramBucket) -> Optional[sql.Composed]:
    """Generate a filter string for a specific histogram bucket.

    Args:
        col (ZenoColumn): the column to use for filtering the data based on the bucket.
        bucket (HistogramBucket): the histogram bucket to limit the data output to.

    Returns:
        Optional[sql.Composed]: filter string to be used to filter the SQL table.
    """
    if col.data_type == MetadataType.BOOLEAN:
        return sql.SQL("{} IS {}").format(
            sql.Identifier(col.id), sql.Literal(bool(bucket.bucket))
        )
    elif col.data_type == MetadataType.NOMINAL:
        return sql.SQL("{} = {}").format(
            sql.Identifier(col.id), sql.Literal(bucket.bucket)
        )
    elif col.data_type == MetadataType.CONTINUOUS:
        return sql.SQL("{} > {} AND {} < {}").format(
            sql.Identifier(col.id),
            sql.Literal(bucket.bucket),
            sql.Identifier(col.id),
            sql.Literal(bucket.bucket_end),
        )
    return None
