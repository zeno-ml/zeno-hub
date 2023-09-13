"""Map metric names to metric functions."""

from functools import lru_cache

from psycopg import sql

from zeno_backend.classes.base import GroupMetric
from zeno_backend.classes.metric import Metric
from zeno_backend.database.database import Database
from zeno_backend.processing.metrics.bleu import bleu
from zeno_backend.processing.metrics.f1 import f1, precision, recall
from zeno_backend.processing.metrics.mean import mean


def count(
    project: str, filter: sql.Composed | None, size_as_metric: bool = False
) -> GroupMetric:
    """Count the number of datapoints matching a specified filter.

    Args:
        project (str): the project the user is currently working with.
        filter (sql.Composed | None): the filter to be applied before counting.
        size_as_metric (bool): whether to return the count as the metric.

    Raises:
        Exception: something in the database processing failed.

    Returns:
        GroupMetric: count of datapoints matching the specified filter.
    """
    with Database() as db:
        num_total = db.execute_return(
            sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(project))
            if filter is None
            else sql.SQL("SELECT COUNT(*) FROM {} WHERE ").format(
                sql.Identifier(project)
            )
            + filter,
        )

        if size_as_metric:
            met = num_total[0][0] if isinstance(num_total[0][0], int) else 0
        else:
            met = None

        return (
            GroupMetric(
                metric=met,
                size=num_total[0][0] if isinstance(num_total[0][0], int) else 0,
            )
            if num_total is not None
            else GroupMetric(metric=None, size=0)
        )


@lru_cache(maxsize=4096)
def metric_map(
    metric: Metric | None,
    project: str,
    model: str | None,
    sql_filter: sql.Composed | None,
) -> GroupMetric:
    """Call a metric function based on the selected metric.

    Args:
        metric (Metric): the metric for which to call a metric function.
        project (str): the project the user is currently working with.
        model (str): the model for which to calculate the metric.
        sql_filter (str | None): the filter to apply to the data before metric
        calculation.

    Returns:
        GroupMetric: the metric result calculated on the data as specified.
    """
    if metric is None or model is None:
        return count(project, sql_filter)

    if metric.type == "mean":
        return mean(project, metric, model, sql_filter)
    if metric.type == "bleu":
        return bleu(project, metric, model, sql_filter)
    if metric.type == "recall":
        return recall(project, model, sql_filter)
    if metric.type == "f1":
        return f1(project, model, sql_filter)
    if metric.type == "precision":
        return precision(project, model, sql_filter)
    if metric.type == "count":
        return count(project, sql_filter, True)

    return count(project, sql_filter)
