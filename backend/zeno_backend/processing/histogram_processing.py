"""Functions for creating the frontend metadata histograms."""
import numpy as np
import pandas as pd
from psycopg import sql

from zeno_backend.classes.base import MetadataType, ZenoColumn
from zeno_backend.classes.metadata import (
    HistogramBucket,
    HistogramRequest,
)
from zeno_backend.database.select import column, metrics_by_name
from zeno_backend.processing.filtering import bucket_filter, filter_to_sql, table_filter
from zeno_backend.processing.metrics import metric_map


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
    res: list[list[HistogramBucket]] = []
    for col in req:
        col_list = column(project, col)
        df_col: pd.Series = pd.DataFrame({"col": col_list})["col"]
        if col.data_type == MetadataType.NOMINAL:
            ret_hist: list[HistogramBucket] = []
            val_counts: pd.Series = df_col.value_counts()
            for k in val_counts.keys():  # type: ignore
                ret_hist.append(HistogramBucket(bucket=k))
            res.append(ret_hist)
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
            res.append(ret_hist)
        elif col.data_type == MetadataType.BOOLEAN:
            res.append(
                [
                    HistogramBucket(bucket=True),
                    HistogramBucket(bucket=False),
                ]
            )
        elif col.data_type == MetadataType.DATETIME:
            res.append([])
        else:
            res.append([])
    return res


def histogram_counts(project: str, req: HistogramRequest) -> list[list[int]]:
    """Calculate count for each bucket in each column histogram.

    Args:
        project (str): the project the user is currently working with.
        req (HistogramRequest): specifying which histograms to calculate counts for.

    Returns:
        List[List[int]]: counts for the individual buckets of specified histograms.
    """
    ret: list[list[int]] = []
    for r in req.column_requests:
        col = r.column
        data_frame = pd.DataFrame(
            {
                "col": column(
                    project,
                    col,
                    None
                    if req.filter_predicates is None
                    else filter_to_sql(req.filter_predicates, project),
                )
            }
        )
        if col.data_type == MetadataType.NOMINAL:
            counts: pd.Series[int] = data_frame.groupby("col").size()  # type: ignore
            ret.append(
                [
                    counts[b.bucket] if b.bucket in counts else 0  # type: ignore
                    for b in r.buckets
                ]
            )
        elif col.data_type == MetadataType.BOOLEAN:
            ret.append(
                [data_frame["col"].sum(), len(data_frame) - data_frame["col"].sum()]
            )
        elif col.data_type == MetadataType.CONTINUOUS:
            bucs = [b.bucket for b in r.buckets]
            ret.append(
                data_frame.groupby([pd.cut(data_frame["col"], bucs)])  # type: ignore
                .size()
                .astype(int)
                .tolist()
            )
        else:
            ret.append([])
    return ret


def histogram_metrics(project: str, req: HistogramRequest) -> list[list[float | None]]:
    """Calculate metric for each bucket in each column histogram.

    Args:
        project (str): the project the user is currently working with.
        req (HistogramRequest): the histograms for which to calculate metrics.

    Returns:
        List[List[Union[float, None]]]: metrics for the requested histogram buckets.
    """
    if req.metric is None:
        return []

    metric_obj = metrics_by_name([req.metric], project)[0]

    filter_sql = table_filter(project, req.model, req.filter_predicates, req.data_ids)
    ret: list[list[float | None]] = []
    for r in req.column_requests:
        loc_ret: list[float | None] = []
        index = 0
        for bucket in r.buckets:
            if req.model:
                filter_bucket = bucket_filter(r.column, bucket)
                if index == 0:
                    index = 1
                final_filter = filter_sql
                if filter_bucket is not None:
                    if final_filter is None:
                        final_filter = filter_bucket
                    else:
                        final_filter = final_filter + sql.SQL(" AND ") + filter_bucket
                metric = metric_map(metric_obj, project, req.model, final_filter)
                if metric.metric is None:
                    loc_ret.append(None)
                else:
                    loc_ret.append(metric.metric)
            else:
                loc_ret.append(None)
        ret.append(loc_ret)
    return ret
