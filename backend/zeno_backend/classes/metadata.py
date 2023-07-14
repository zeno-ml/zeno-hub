"""Type representations for metric data."""
from typing import List, Optional, Union

from zeno_backend.classes.base import CamelModel, ZenoColumn
from zeno_backend.classes.metric import Metric
from zeno_backend.classes.slice import FilterPredicateGroup


class HistogramBucket(CamelModel):
    """Specification of a histogram bucket in Zeno."""

    bucket: Union[float, bool, int, str]
    bucket_end: Optional[Union[float, bool, int, str]] = None


class HistogramColumnRequest(CamelModel):
    """Specification of a histogram column request in Zeno."""

    column: ZenoColumn
    buckets: List[HistogramBucket]


class HistogramRequest(CamelModel):
    """Specification of a histogram request in Zeno."""

    column_requests: List[HistogramColumnRequest]
    filter_predicates: Optional[FilterPredicateGroup] = None
    model: Optional[str] = None
    metric: Optional[Metric] = None
    items: Optional[List[str]] = None
