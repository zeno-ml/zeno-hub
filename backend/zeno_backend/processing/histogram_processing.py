"""Functions for creating the frontend metadata histograms."""

import math

from psycopg import sql

from zeno_backend.classes.base import MetadataType, ZenoColumn
from zeno_backend.classes.metadata import (
    HistogramBucket,
    HistogramColumnRequest,
    HistogramRequest,
)
from zeno_backend.database.database import db_pool


async def histogram_bucket(project_uuid: str, col: ZenoColumn):
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
                sql.SQL("SELECT column_id FROM {} WHERE name = %s;").format(
                    sql.Identifier(f"{project_uuid}_column_map")
                ),
                [col.name],
            )
            id_col = await db.fetchone()
            if id_col is None:
                return []
            else:
                id_col = id_col[0]

            if col.data_type == MetadataType.NOMINAL:
                await db.execute(
                    sql.SQL("SELECT {} FROM {} GROUP BY {}").format(
                        sql.Identifier(id_col),
                        sql.Identifier(project_uuid),
                        sql.Identifier(id_col),
                    )
                )
                res = await db.fetchall()
                if len(res) > 30:
                    return []
                else:
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

                # Replicate the numpy histogram binning, max of Sturges and FD
                # https://numpy.org/doc/stable/reference/generated/numpy.histogram_bin_edges.html
                buckets_sturges = 1 + math.ceil(math.log2(res[3]))
                buckets_fd = math.ceil(2 * res[2] / res[3] ** (1 / 3))
                buckets = max(buckets_sturges, buckets_fd)
                step = (res[1] - res[0]) / buckets

                return [
                    HistogramBucket(
                        bucket=res[0] + i * step, bucket_end=res[0] + (i + 1) * step
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
    col_request: HistogramColumnRequest,
    project_uuid: str,
    filter_sql: sql.Composed | None,
    calculate_histograms: bool,
) -> list[HistogramBucket]:
    """Calculate the metric and count for a column.

    Args:
        request (HistogramRequest): the request object.
        col_request (HistogramColumnRequest): the column request object.
        project_uuid (str): the project the user is currently working with.
        filter_sql (sql.Composed): the filter to apply to the query.
        calculate_histograms (bool): whether to calculate the metric.

    Returns:
        HistogramBucket: the bucket with the metric added.
    """
    col = col_request.column

    if (
        request.metric is not None
        and request.model is not None
        and calculate_histograms
    ):
        calculate_histograms = True
    else:
        calculate_histograms = False

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
            if calculate_histograms and request.metric is not None:
                await db.execute(
                    sql.SQL(
                        "SELECT column_id FROM {} "
                        "WHERE name = %s AND (model = %s OR model IS NULL);"
                    ).format(sql.Identifier(f"{project_uuid}_column_map")),
                    [request.metric.columns[0], request.model],
                )
                metric_col_id = await db.fetchone()
                if metric_col_id is None:
                    return []
                metric_col_id = metric_col_id[0]

            if col.data_type == MetadataType.NOMINAL:
                await db.execute(
                    sql.SQL("SELECT COUNT(DISTINCT {}) FROM {}").format(
                        sql.Identifier(col_id),
                        sql.Identifier(project_uuid),
                    )
                )
                unique = await db.fetchall()
                if len(unique) > 0 and unique[0][0] > 30:
                    return []
                else:
                    if calculate_histograms and metric_col_id is not None:
                        statement = sql.SQL(
                            "SELECT {}, COUNT(*), AVG({}) FROM {}"
                        ).format(
                            sql.Identifier(col_id),
                            sql.Identifier(metric_col_id),
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
                    if calculate_histograms:
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
                            for b in col_request.buckets
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
                            for b in col_request.buckets
                        ]

            elif col.data_type == MetadataType.CONTINUOUS:
                case_statement = sql.SQL("CASE ")
                for i, b in enumerate(col_request.buckets):
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
                        sql.Identifier(metric_col_id),
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

                if calculate_histograms:
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
                        for i, b in enumerate(col_request.buckets)
                    ]
                else:
                    results_map = {int(r[0]): r[1] for r in db_res if r[0] is not None}
                    return [
                        HistogramBucket(
                            bucket=b.bucket,
                            bucket_end=b.bucket_end,
                            size=results_map[i] if i in results_map else 0,
                        )
                        for i, b in enumerate(col_request.buckets)
                    ]

            elif col.data_type == MetadataType.BOOLEAN:
                if calculate_histograms and metric_col_id is not None:
                    statement = sql.SQL(
                        "SELECT CASE WHEN {} = TRUE THEN 0 WHEN {} = FALSE"
                        " THEN 1 END AS bucket, COUNT(*), AVG({}) FROM {}"
                    ).format(
                        sql.Identifier(col_id),
                        sql.Identifier(col_id),
                        sql.Identifier(metric_col_id),
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
                if calculate_histograms:
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
