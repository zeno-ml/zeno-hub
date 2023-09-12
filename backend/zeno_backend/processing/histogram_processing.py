"""Functions for creating the frontend metadata histograms."""


import numpy as np
import pandas as pd
from psycopg import sql

from zeno_backend.classes.base import MetadataType, ZenoColumn
from zeno_backend.classes.metadata import (
    HistogramBucket,
    HistogramColumnRequest,
    HistogramRequest,
)
from zeno_backend.database.select import column, project_from_uuid
from zeno_backend.processing.filtering import bucket_filter, table_filter
from zeno_backend.processing.metrics.map import metric_map


def histogram_bucket(project_uuid: str, col: ZenoColumn, num_bins: int | str):
    """Calculate the histogram buckets for a single column.

    Args:
        project_uuid (str): the project the user is currently working with.
        col (ZenoColumn): the column to compute buckets for.
        num_bins (int): the number of bins to use for the histogram.


    Returns:
        List[HistogramBucket]: the buckets for the column histogram.
    """
    col_list = column(project_uuid, col)
    df_col: pd.Series = pd.DataFrame({"col": col_list})["col"]
    if col.data_type == MetadataType.NOMINAL:
        ret_hist: list[HistogramBucket] = []
        val_counts: pd.Series = df_col.value_counts()
        if len(val_counts) > 30:
            return []
        else:
            for k in val_counts.keys():  # type: ignore
                ret_hist.append(HistogramBucket(bucket=k))
            return ret_hist
    elif col.data_type == MetadataType.CONTINUOUS:
        ret_hist: list[HistogramBucket] = []
        df_col = pd.to_numeric(df_col).fillna(0)  # type: ignore
        bins = np.histogram_bin_edges(df_col, bins=num_bins)
        for i in range(len(bins) - 1):
            ret_hist.append(
                HistogramBucket(
                    bucket=bins[i],
                    bucket_end=bins[i + 1],
                )
            )
        return ret_hist
    elif col.data_type == MetadataType.BOOLEAN:
        return [
            HistogramBucket(bucket=True),
            HistogramBucket(bucket=False),
        ]

    elif col.data_type == MetadataType.DATETIME:
        return []
    else:
        return []


def histogram_buckets(
    project: str, req: list[ZenoColumn], num_bins: int | str = "doane"
) -> list[list[HistogramBucket]]:
    """Calculate the histogram buckets for a list of columns.

    Args:
        project (str): the project the user is currently working with.
        req (List[ZenoColumn]): list of columns to compute buckets for
        num_bins (Union[int, str], optional):
            estimates the best number and size of bins to use.
            Defaults to "doane", but can be a fixed integer
            Other options can be found
            [here](https://numpy.org/doc/stable/reference/generated/numpy.histogram_bin_edges.html)

    Returns:
        List[List[HistogramBucket]]: for each zeno column return a list of buckets
    """
    res = []
    for col in req:
        res.append(histogram_bucket(project, col, num_bins))
    return res


def histogram_metric_task(
    request: HistogramRequest,
    col_request: HistogramColumnRequest,
    bucket: HistogramBucket,
    project_uuid: str,
    filter_sql: sql.Composed | None,
) -> HistogramBucket:
    """Calculate the metric for a single bucket.

    Args:
        request (HistogramRequest): the request object.
        col_request (HistogramColumnRequest): the column request object.
        bucket (HistogramBucket): the bucket to calculate the metric for.
        project_uuid (str): the project the user is currently working with.
        filter_sql (sql.Composed): the filter to apply to the query.


    Returns:
        HistogramBucket: the bucket with the metric added.
    """
    filter_bucket = bucket_filter(col_request.column, bucket)
    final_filter = filter_sql
    if filter_bucket is not None:
        if final_filter is None:
            final_filter = filter_bucket
        else:
            final_filter = final_filter + sql.SQL(" AND ") + filter_bucket
    metric = metric_map(request.metric, project_uuid, request.model, final_filter)
    return HistogramBucket(
        bucket=bucket.bucket,
        bucket_end=bucket.bucket_end,
        size=metric.size,
        metric=metric.metric,
    )


def histogram_count(
    request: HistogramRequest,
    col_request: HistogramColumnRequest,
    project_uuid: str,
    filter_sql: sql.Composed | None,
    calculate_histograms: bool,
) -> list[HistogramBucket]:
    """Calculate the counts and metrics for a column.

    Args:
        request (HistogramRequest): the request object.
        col_request (HistogramColumnRequest): the column request object.
        project_uuid (str): the project the user is currently working with.
        filter_sql (sql.Composed): the filter to apply to the query.
        calculate_histograms (bool): whether to calculate the histograms or not.


    Returns:
        List[HistogramBucket]: the buckets with the counts and metrics added.
    """
    col = col_request.column

    if request.model is None or request.metric is None or not calculate_histograms:
        col = col_request.column
        data_frame = pd.DataFrame({"col": column(project_uuid, col, filter_sql)})
        if col.data_type == MetadataType.NOMINAL:
            if data_frame["col"].nunique() > 30:
                return []
            else:
                counts: pd.Series[int] = data_frame.groupby("col").size()
                return [
                    HistogramBucket(
                        bucket=b.bucket,
                        size=counts[b.bucket]  # type: ignore
                        if b.bucket in counts
                        else 0,
                    )
                    for b in col_request.buckets
                ]

        elif col.data_type == MetadataType.CONTINUOUS:
            bucs = [b.bucket for b in col_request.buckets]
            intervals = pd.IntervalIndex.from_arrays(
                [float(b.bucket) for b in col_request.buckets],
                [float(b.bucket_end) for b in col_request.buckets],  # type: ignore
            )
            counts = (
                data_frame.groupby(
                    [pd.cut(data_frame["col"], intervals)],
                    observed=False,  # type: ignore
                )
                .size()
                .astype(int)
                .tolist()
            )
            return [
                HistogramBucket(
                    bucket=b,
                    size=counts[i],
                )
                for i, b in enumerate(bucs)
            ]
        elif col.data_type == MetadataType.BOOLEAN:
            return [
                HistogramBucket(
                    bucket=True,
                    size=data_frame["col"].sum(),
                ),
                HistogramBucket(
                    bucket=False,
                    size=len(data_frame) - data_frame["col"].sum(),
                ),
            ]
        else:
            return []
    else:
        res = []
        for b in col_request.buckets:
            res.append(
                histogram_metric_task(request, col_request, b, project_uuid, filter_sql)
            )
        return res


def histogram_counts(
    project_uuid: str, req: HistogramRequest
) -> list[list[HistogramBucket]]:
    """Calculate count and optionally metric for each bucket in each column histogram.

    Args:
        project_uuid (str): the project the user is currently working with.
        req (HistogramRequest): specifying which histograms to calculate counts for.

    Returns:
        List[List[int]]: counts for the individual buckets of specified histograms.
    """
    project_obj = project_from_uuid(project_uuid)
    if project_obj is None:
        return []
    filter_sql = table_filter(
        project_uuid, req.model, req.filter_predicates, req.data_ids
    )
    res = []
    for r in req.column_requests:
        res.append(
            histogram_count(
                req,
                r,
                project_uuid,
                filter_sql,
                project_obj.calculate_histogram_metrics,
            )
        )

    return res
