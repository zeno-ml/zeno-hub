"""Type representations for metric data."""
from zeno_backend.classes.base import CamelModel, ZenoColumn
from zeno_backend.classes.metric import Metric
from zeno_backend.classes.slice import FilterPredicateGroup


class HistogramBucket(CamelModel):
    """Specification of a histogram bucket in Zeno."""

    bucket: float | bool | int | str
    bucket_end: float | bool | int | str | None = None


class HistogramColumnRequest(CamelModel):
    """Specification of a histogram column request in Zeno."""

    column: ZenoColumn
    buckets: list[HistogramBucket]


class HistogramRequest(CamelModel):
    """Specification of a histogram request in Zeno."""

    column_requests: list[HistogramColumnRequest]
    filter_predicates: FilterPredicateGroup | None = None
    model: str | None = None
    metric: Metric | None = None
    data_ids: list[str] | None = None


class StringFilterRequest(CamelModel):
    """Specification of a string filter request in Zeno."""

    column: ZenoColumn
    filter_string: str
    is_regex: bool
    case_match: bool
    whole_word_match: bool
