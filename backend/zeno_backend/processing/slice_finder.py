"""Methods to run slice-finder in order to slice the user's data."""
import secrets
from typing import List, Union

import numpy as np
import pandas as pd
from sliceline.slicefinder import Slicefinder

from zeno_backend.classes.base import MetadataType, ZenoColumn
from zeno_backend.classes.filter import FilterPredicate, Join, Operation
from zeno_backend.classes.slice import FilterPredicateGroup, Slice
from zeno_backend.classes.slice_finder import SliceFinderRequest, SliceFinderReturn
from zeno_backend.database.select import table_data
from zeno_backend.processing.filtering import table_filter
from zeno_backend.processing.util import generate_diff_cols


def cont_cols_df(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """Discretize continuous valued columns.

    Args:
        df (pd.DataFrame): _description_
        cols (List[str]): _description_

    Returns:
        pd.DataFrame: _description_
    """
    new_df = pd.DataFrame()
    for col in cols:
        df_col: List[float] = pd.to_numeric(df.loc[:, col].copy())  # type: ignore
        bins = list(np.histogram_bin_edges(df_col, bins="doane"))
        bins[0], bins[len(bins) - 1] = bins[0] - 1, bins[len(bins) - 1] + 1
        new_df.loc[:, col + "_encode"] = pd.cut(df_col, bins=bins)
    return new_df


def slice_finder(project: str, req: SliceFinderRequest) -> SliceFinderReturn:
    """Return slices of data with high or low metric values.

    Args:
        project (str): the project the user is currently working with
        req (SliceFinderRequest): Request with columns, metrics, and options.

    Returns a SliceFinderMetricReturn Object.
    """
    cont_search_cols: List[ZenoColumn] = []
    not_cont_search_cols: List[ZenoColumn] = []
    for col in req.search_columns:
        if col.data_type == MetadataType.CONTINUOUS:
            cont_search_cols.append(col)
        else:
            not_cont_search_cols.append(col)

    search_cols: List[ZenoColumn] = not_cont_search_cols + cont_search_cols
    cont_search_col_ids: List[str] = [col.id for col in cont_search_cols]
    not_cont_search_col_ids: List[str] = [col.id for col in not_cont_search_cols]
    metric_col: str = "diff" if req.compare_column else req.metric_column.id

    filter_sql = table_filter(project, None, req.filter_predicates, req.items)
    sql_table = table_data(project, filter_sql)
    filt_df = pd.DataFrame(sql_table.table, columns=sql_table.columns)
    cont_df = cont_cols_df(filt_df[cont_search_col_ids].dropna(), cont_search_col_ids)

    if req.compare_column:
        filt_df = generate_diff_cols(
            filt_df, req.metric_column, req.compare_column, project
        )

    unique_cols = set(not_cont_search_col_ids + [metric_col])
    updated_df = pd.concat(
        [filt_df[list(unique_cols)], cont_df], axis=1
    ).dropna()  # type: ignore

    normalized_metric_col = np.array(updated_df[metric_col], dtype=float)

    # Invert metric column if ascending.
    metric_max = np.max(normalized_metric_col)
    if req.order_by == "ascending":
        normalized_metric_col = metric_max - normalized_metric_col

    cont_search_col_ids = [col + "_encode" for col in cont_search_col_ids]
    search_cols_str = not_cont_search_col_ids + cont_search_col_ids
    slice_finder = Slicefinder(alpha=req.alpha, k=20, max_l=req.max_lattice)
    slice_finder.fit(updated_df[search_cols_str].to_numpy(), normalized_metric_col)

    if slice_finder.top_slices_ is None or slice_finder.top_slices_statistics_ is None:
        return SliceFinderReturn(slices=[], metrics=[], sizes=[], overall_metric=0)

    discovered_slices: List[Slice] = []
    slice_metrics: List[float] = []
    slice_sizes: List[int] = []
    not_cont_search_num = len(not_cont_search_cols)

    for sli_i, sli in enumerate(slice_finder.top_slices_):
        # Rescale back to original metric.
        if req.order_by == "ascending":
            slice_metrics.append(
                metric_max
                - slice_finder.top_slices_statistics_[sli_i]["slice_average_error"]
            )
        else:
            slice_metrics.append(
                slice_finder.top_slices_statistics_[sli_i]["slice_average_error"]
            )

        slice_sizes.append(slice_finder.top_slices_statistics_[sli_i]["slice_size"])

        predicate_list: List[Union[FilterPredicate, FilterPredicateGroup]] = []
        for pred_i, sli_predicate in enumerate(sli):
            if sli_predicate is not None:
                join_val = Join.OMITTED if len(predicate_list) == 0 else Join.AND
                col = search_cols[pred_i]

                # not continuous columns
                if pred_i < not_cont_search_num:
                    if str(sli_predicate) in ["True", "False"]:
                        sli_predicate = "true" if sli_predicate else "false"
                    predicate_list.append(
                        FilterPredicate(
                            column=col,
                            operation=Operation.EQUAL,
                            value=sli_predicate,
                            join=join_val,
                        )
                    )
                # continuous columns
                else:
                    left_pred = FilterPredicate(
                        column=col,
                        operation=Operation.GTE,
                        value=sli_predicate.left,
                        join=Join.OMITTED,
                    )
                    right_pred = FilterPredicate(
                        column=col,
                        operation=Operation.LT,
                        value=sli_predicate.right,
                        join=Join.AND,
                    )
                    predicate_list.append(
                        FilterPredicateGroup(
                            predicates=[left_pred, right_pred], join=join_val
                        ),
                    )

        discovered_slices.append(
            Slice(
                id=sli_i,
                slice_name="Generated Slice " + secrets.token_hex(nbytes=4),
                folder_id=None,
                filter_predicates=FilterPredicateGroup(
                    predicates=predicate_list, join=Join.OMITTED
                ),
            )
        )
    return SliceFinderReturn(
        slices=discovered_slices,
        metrics=slice_metrics,
        sizes=slice_sizes,
        overall_metric=slice_finder.average_error_
        if slice_finder.average_error_
        else 0,
    )
