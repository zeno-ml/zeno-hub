"""Mean metric calculation."""

from psycopg import sql

from zeno_backend.classes.base import GroupMetric, MetadataType
from zeno_backend.classes.metric import Metric
from zeno_backend.database.database import db_pool


async def mean(
    project_uuid: str, metric: Metric, model: str | None, filter: sql.Composed | None
) -> GroupMetric:
    """Calculate the mean of a metric for a given project.

    Args:
        project_uuid (str): the project the user is currently working with.
        metric (Metric): the metric for which to calculate the mean.
        model (str): the model for which to calculate the metric.
        filter (sql.Composed | None): the filter to apply to the data before metric.

    Raises:
        Exception: something in the database processing failed.

    Returns:
        GroupMetric: mean of the metric for the given project.
    """
    async with db_pool.connection() as db:
        async with db.cursor() as cur:
            # Get column name from project column map
            await cur.execute(
                sql.SQL(
                    "SELECT column_id, data_type FROM {} WHERE name = {} AND"
                    " (model IS NULL OR model = {})"
                ).format(
                    sql.Identifier(f"{project_uuid}_column_map"),
                    sql.Literal(metric.columns[0]),
                    sql.Literal(model),
                )
            )
            column_output = await cur.fetchall()

            if len(column_output) == 0:
                if filter is not None:
                    await cur.execute(
                        sql.SQL("SELECT COUNT(*) AS n FROM {} WHERE ").format(
                            sql.Identifier(project_uuid),
                        )
                        + filter
                    )
                else:
                    await cur.execute(
                        sql.SQL("SELECT COUNT(*) AS n FROM {}").format(
                            sql.Identifier(project_uuid),
                        )
                    )
                row_count = await cur.fetchall()
                if len(row_count) > 0:
                    return GroupMetric(metric=None, size=row_count[0][0])
                else:
                    return GroupMetric(metric=None, size=0)

            column_id = column_output[0][0]
            if column_output[0][1] == MetadataType.BOOLEAN:
                column_id = sql.Identifier(column_id) + sql.SQL("::int")
            else:
                column_id = sql.Identifier(column_id)

            if filter is None:
                await cur.execute(
                    sql.SQL("SELECT COUNT(*) AS n, AVG({}) FROM {}").format(
                        column_id, sql.Identifier(project_uuid)
                    )
                )
            else:
                await cur.execute(
                    sql.SQL("SELECT COUNT(*) AS n, AVG({}) FROM {} WHERE ").format(
                        column_id, sql.Identifier(project_uuid)
                    )
                    + filter
                )

            if cur.rowcount == 0:
                return GroupMetric(metric=None, size=0)
            else:
                res = await cur.fetchone()

            if res is not None:
                return GroupMetric(
                    metric=float(res[1]) if res[1] is not None else None, size=res[0]
                )
            else:
                return GroupMetric(metric=None, size=0)
