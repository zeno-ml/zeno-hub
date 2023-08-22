"""Type representations for slice finder data."""
from typing import Any

from zeno_backend.classes.base import CamelModel, ZenoColumn
from zeno_backend.classes.slice import FilterPredicateGroup, Slice


class SliceFinderRequest(CamelModel):
    """Specification of a request to the slice finder functionality."""

    metric_column: ZenoColumn
    search_columns: list[ZenoColumn]
    order_by: str
    alpha: float
    max_lattice: int
    compare_column: ZenoColumn | None = None
    filter_predicates: FilterPredicateGroup | None = None
    data_ids: list[str] | None = None


class SliceFinderReturn(CamelModel):
    """Specification of the return type of a slice finder request."""

    slices: list[Slice]
    metrics: list[float]
    sizes: list[int]
    overall_metric: float | None = None


class SQLTable(CamelModel):
    """Specification of table data in Zeno."""

    table: list[Any]
    columns: list[str]
