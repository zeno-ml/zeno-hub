"""Type representations for metric data."""
from typing import List, Optional

from zeno_backend.classes.base import CamelModel
from zeno_backend.classes.slice import Slice


class Metric(CamelModel):
    """Specification of metric data in Zeno."""

    id: int
    name: str


class MetricKey(CamelModel):
    """Specification of metric keys in zeno.

    Metric keys map to a specific slice, model, and metric.
    """

    slice: Slice
    model: str
    metric: Metric


class MetricRequest(CamelModel):
    """Specification of a metric request in Zeno.

    Can be used to request metric calculation on specific data subsets.
    """

    metric_keys: List[MetricKey]
    data_ids: Optional[List[str]] = None
