"""Type representations for slice finder data."""
from typing import Any, List, Optional

from zeno_backend.classes.base import CamelModel, ZenoColumn
from zeno_backend.classes.slice import FilterPredicateGroup, Slice


class SliceFinderRequest(CamelModel):
    """Specification of a request to the slice finder functionality."""

    metric_column: ZenoColumn
    search_columns: List[ZenoColumn]
    order_by: str
    alpha: float
    max_lattice: int
    compare_column: Optional[ZenoColumn] = None
    filter_predicates: Optional[FilterPredicateGroup] = None
    items: Optional[List[str]] = None


class SliceFinderReturn(CamelModel):
    """Specification of the return type of a slice finder request."""

    slices: List[Slice]
    metrics: List[float]
    sizes: List[int]
    overall_metric: Optional[float] = None


class SQLTable(CamelModel):
    """Specification of table data in Zeno."""

    table: List[Any]
    columns: List[str]
