"""Type representations for slice finder data."""
from typing import Any

from zeno_backend.classes.base import CamelModel, ZenoColumn
from zeno_backend.classes.slice import FilterPredicateGroup, Slice


class SliceFinderRequest(CamelModel):
    """Specification of a request to the slice finder functionality.

    Attributes:
        metric_column (ZenoColumn): the metric column to be used.
        search_columns (list[ZenoColumn]): the search columns to be used.
        order_by (str): the order by clause to be used.
        alpha (float): the alpha value to be used for the slice finder.
        max_lattice (int): the maximum lattice size to be used for the slice finder.
        compare_column (ZenoColumn | None): the compare column to be used.
        filter_predicates (FilterPredicateGroup | None): the filter predicates to be
            applied to the data.
        data_ids (list[str] | None): the data ids to be used for the slice finder.
    """

    metric_column: ZenoColumn
    search_columns: list[ZenoColumn]
    order_by: str
    alpha: float
    max_lattice: int
    compare_column: ZenoColumn | None = None
    filter_predicates: FilterPredicateGroup | None = None
    data_ids: list[str] | None = None


class SliceFinderReturn(CamelModel):
    """Specification of the return type of a slice finder request.

    Attributes:
        slices (list[Slice]): the slices found by the slice finder.
        metrics (list[float]): the metrics of the slices found by the slice finder.
        sizes (list[int]): the sizes of the slices found by the slice finder.
        overall_metric (float | None): the overall metric of the slice finder.
    """

    slices: list[Slice]
    metrics: list[float]
    sizes: list[int]
    overall_metric: float | None = None


class SQLTable(CamelModel):
    """Specification of table data in Zeno.

    Attributes:
        table (list[Any]): the table data.
        columns (list[str]): the column names.
    """

    table: list[Any]
    columns: list[str]
