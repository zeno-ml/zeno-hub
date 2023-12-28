"""Functions for creating the frontend metadata histograms."""

import math

from psycopg import sql

from zeno_backend.classes.base import MetadataType, ZenoColumn
from zeno_backend.classes.metadata import (
    HistogramBucket,
    HistogramRequest,
)
from zeno_backend.database.database import db_pool


async def calculate_histogram_bucket(
    project_uuid: str, col: ZenoColumn
) -> list[HistogramBucket]:
    """Calculate the histogram buckets for a single column.

    Args:
        project_uuid (str): the project the user is currently working with.
        col (ZenoColumn): the column to compute buckets for.

    Returns:
        List[HistogramBucket]: the buckets for the column histogram.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as db:
            await db.execute(
                sql.SQL(
                    "SELECT column_id FROM {} WHERE name = %s AND"
                    " (model = %s OR model IS NULL);"
                ).format(sql.Identifier(f"{project_uuid}_column_map")),
                [col.name, col.model],
            )
            id_col = await db.fetchone()
            if id_col is None:
                return []
            else:
                id_col = id_col[0]

            if col.data_type == MetadataType.NOMINAL:
                await db.execute(
                    sql.SQL(
                        "SELECT COUNT(*) FROM (SELECT DISTINCT {} FROM {}) AS temp;"
                    ).format(
                        sql.Identifier(id_col),
                        sql.Identifier(project_uuid),
                    )
                )
                res = await db.fetchall()
                if res[0][0] > 30:
                    return []
                else:
                    await db.execute(
                        sql.SQL("SELECT DISTINCT {} FROM {}").format(
                            sql.Identifier(id_col),
                            sql.Identifier(project_uuid),
                        )
                    )
                    res = await db.fetchall()
                    return [HistogramBucket(bucket=r[0]) for r in res]

            elif col.data_type == MetadataType.CONTINUOUS:
                await db.execute(
                    sql.SQL(
                        "SELECT MIN({}), MAX({}),"
                        "PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY {})"
                        "- PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY {})"
                        ",COUNT(*) FROM {}"
                    ).format(
                        sql.Identifier(id_col),
                        sql.Identifier(id_col),
                        sql.Identifier(id_col),
                        sql.Identifier(id_col),
                        sql.Identifier(project_uuid),
                    )
                )
                res = await db.fetchone()
                if res is None:
                    return []

                # Sturges estimator
                buckets = int(math.ceil(math.log2(res[3] + 1)))
                bin_width = (res[1] - res[0]) / buckets

                return [
                    HistogramBucket(
                        bucket=res[0] + i * bin_width,
                        bucket_end=res[0] + (i + 1) * bin_width,
                    )
                    for i in range(0, buckets)
                ]
            elif col.data_type == MetadataType.BOOLEAN:
                return [
                    HistogramBucket(bucket=True),
                    HistogramBucket(bucket=False),
                ]
            else:
                return []


async def histogram_metric_and_count(
    request: HistogramRequest,
    col: ZenoColumn,
    buckets: list[HistogramBucket] | None,
    project_uuid: str,
    filter_sql: sql.Composed | None,
) -> list[HistogramBucket]:
    """Calculate the metric and count for a column.

    Args:
        request (HistogramRequest): the request object.
        col (ZenoColumn): the column request object.
        buckets (list[HistogramBucket]): the buckets to calculate the metric for.
        project_uuid (str): the project the user is currently working with.
        filter_sql (sql.Composed): the filter to apply to the query.

    Returns:
        HistogramBucket: the bucket with the metric added.
    """
    if request.metric is not None and request.model is not None:
        calculate_histograms = True
    else:
        calculate_histograms = False

    if buckets is None or len(buckets) == 0:
        return []
    async with db_pool.connection() as conn:
        async with conn.cursor() as db:
            await db.execute(
                sql.SQL(
                    "SELECT column_id FROM {} "
                    "WHERE name = %s AND (model = %s OR model IS NULL);"
                ).format(sql.Identifier(f"{project_uuid}_column_map")),
                [col.name, request.model],
            )
            col_id = await db.fetchone()
            if col_id is None:
                return []
            col_id = col_id[0]

            metric_col_id = None
            metric_col_type = None
            if calculate_histograms and request.metric is not None:
                await db.execute(
                    sql.SQL(
                        "SELECT column_id, data_type FROM {} "
                        "WHERE name = %s AND (model = %s OR model IS NULL);"
                    ).format(sql.Identifier(f"{project_uuid}_column_map")),
                    [request.metric.columns[0], request.model],
                )
                metric_col_id = await db.fetchone()
                if metric_col_id is not None:
                    metric_col_type = metric_col_id[1]
                    metric_col_id = metric_col_id[0]

            if col.data_type == MetadataType.NOMINAL:
                if calculate_histograms and metric_col_id is not None:
                    statement = sql.SQL("SELECT {}, COUNT(*), AVG({}) FROM {}").format(
                        sql.Identifier(col_id),
                        sql.Identifier(metric_col_id)
                        if metric_col_type != MetadataType.BOOLEAN
                        else sql.Identifier(metric_col_id) + sql.SQL("::int"),
                        sql.Identifier(project_uuid),
                    )
                else:
                    statement = sql.SQL("SELECT {}, COUNT(*) FROM {}").format(
                        sql.Identifier(col_id),
                        sql.Identifier(project_uuid),
                    )

                if filter_sql:
                    statement = sql.SQL("{} WHERE {} GROUP BY {}").format(
                        statement, filter_sql, sql.Identifier(col_id)
                    )
                else:
                    statement = sql.SQL("{} GROUP BY {}").format(
                        statement, sql.Identifier(col_id)
                    )

                await db.execute(statement)
                db_res = await db.fetchall()
                if calculate_histograms and metric_col_id is not None:
                    results_map = {r[0]: (r[1], r[2]) for r in db_res}
                    return [
                        HistogramBucket(
                            bucket=b.bucket,
                            size=results_map[b.bucket][0]
                            if b.bucket in results_map
                            else 0,
                            metric=results_map[b.bucket][1]
                            if b.bucket in results_map
                            else 0,
                        )
                        for b in buckets
                    ]
                else:
                    results_map = {r[0]: r[1] for r in db_res}
                    return [
                        HistogramBucket(
                            bucket=b.bucket,
                            size=results_map[b.bucket]
                            if b.bucket in results_map
                            else 0,
                        )
                        for b in buckets
                    ]

            elif col.data_type == MetadataType.CONTINUOUS:
                case_statement = sql.SQL("CASE ")
                for i, b in enumerate(buckets):
                    if i == len(buckets) - 1:
                        case_statement += sql.SQL(
                            "WHEN {} >= {} AND {} <= {} THEN {} "
                        ).format(
                            sql.Identifier(col_id),
                            sql.Literal(b.bucket),
                            sql.Identifier(col_id),
                            sql.Literal(b.bucket_end),
                            sql.Literal(i),
                        )
                    else:
                        case_statement += sql.SQL(
                            "WHEN {} >= {} AND {} < {} THEN {} "
                        ).format(
                            sql.Identifier(col_id),
                            sql.Literal(b.bucket),
                            sql.Identifier(col_id),
                            sql.Literal(b.bucket_end),
                            sql.Literal(i),
                        )
                case_statement += sql.SQL("END AS bucket")
                if calculate_histograms and metric_col_id is not None:
                    statement = sql.SQL("SELECT {}, COUNT(*), AVG({}) FROM {}").format(
                        case_statement,
                        sql.Identifier(metric_col_id)
                        if metric_col_type != MetadataType.BOOLEAN
                        else sql.Identifier(metric_col_id) + sql.SQL("::int"),
                        sql.Identifier(project_uuid),
                    )
                else:
                    statement = sql.SQL("SELECT {}, COUNT(*) FROM {}").format(
                        case_statement,
                        sql.Identifier(project_uuid),
                    )

                if filter_sql:
                    statement = sql.SQL("{} WHERE {} GROUP BY bucket").format(
                        statement, filter_sql
                    )
                else:
                    statement = sql.SQL("{} GROUP BY bucket").format(statement)
                await db.execute(statement)
                db_res = await db.fetchall()

                if calculate_histograms and metric_col_id is not None:
                    results_map = {
                        int(r[0]): (r[1], r[2]) for r in db_res if r[0] is not None
                    }
                    return [
                        HistogramBucket(
                            bucket=b.bucket,
                            bucket_end=b.bucket_end,
                            size=results_map[i][0] if i in results_map else 0,
                            metric=results_map[i][1] if i in results_map else 0,
                        )
                        for i, b in enumerate(buckets)
                    ]
                else:
                    results_map = {int(r[0]): r[1] for r in db_res if r[0] is not None}
                    return [
                        HistogramBucket(
                            bucket=b.bucket,
                            bucket_end=b.bucket_end,
                            size=results_map[i] if i in results_map else 0,
                        )
                        for i, b in enumerate(buckets)
                    ]

            elif col.data_type == MetadataType.BOOLEAN:
                if calculate_histograms and metric_col_id is not None:
                    statement = sql.SQL(
                        "SELECT CASE WHEN {} = TRUE THEN 0 WHEN {} = FALSE"
                        " THEN 1 END AS bucket, COUNT(*), AVG({}) FROM {}"
                    ).format(
                        sql.Identifier(col_id),
                        sql.Identifier(col_id),
                        sql.Identifier(metric_col_id)
                        if metric_col_type != MetadataType.BOOLEAN
                        else sql.Identifier(metric_col_id) + sql.SQL("::int"),
                        sql.Identifier(project_uuid),
                    )
                else:
                    statement = sql.SQL(
                        "SELECT CASE WHEN {} = TRUE THEN 0 WHEN {} = FALSE"
                        " THEN 1 END AS bucket, COUNT(*) FROM {}"
                    ).format(
                        sql.Identifier(col_id),
                        sql.Identifier(col_id),
                        sql.Identifier(project_uuid),
                    )

                if filter_sql:
                    statement = sql.SQL("{} WHERE {} GROUP BY bucket").format(
                        statement, filter_sql
                    )
                else:
                    statement = sql.SQL("{} GROUP BY bucket").format(statement)
                await db.execute(statement)
                res = await db.fetchall()

                true_res = [r for r in res if r[0] == 0]
                false_res = [r for r in res if r[0] == 1]
                if calculate_histograms and metric_col_id is not None:
                    return [
                        HistogramBucket(
                            bucket=True,
                            size=true_res[0][1] if len(true_res) > 0 else 0,
                            metric=true_res[0][2] if len(true_res) > 0 else 0,
                        ),
                        HistogramBucket(
                            bucket=False,
                            size=false_res[0][1] if len(false_res) > 0 else 0,
                            metric=false_res[0][2] if len(false_res) > 0 else 0,
                        ),
                    ]
                else:
                    return [
                        HistogramBucket(
                            bucket=True,
                            size=true_res[0][1] if len(true_res) > 0 else 0,
                        ),
                        HistogramBucket(
                            bucket=False,
                            size=false_res[0][1] if len(false_res) > 0 else 0,
                        ),
                    ]
            else:
                return []
