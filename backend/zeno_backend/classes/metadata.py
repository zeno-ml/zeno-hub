"""Type representations for metric data."""
from zeno_backend.classes.base import CamelModel, ZenoColumn
from zeno_backend.classes.filter import Operation
from zeno_backend.classes.metric import Metric
from zeno_backend.classes.slice import FilterPredicateGroup


class HistogramBucket(CamelModel):
    """Specification of a histogram bucket in Zeno.

    Attributes:
        bucket (float | bool | int | str): the bucket value.
        bucket_end (float | bool | int | str | None): the bucket end value.
        size (int | None): the size of the bucket.
        filtered_size (int | None): the size of the bucket after filtering.
        metric (float | None): the metric value of the bucket.
    """

    bucket: float | bool | int | str
    bucket_end: float | bool | int | str | None = None
    size: int | None = None
    filtered_size: int | None = None
    metric: float | None = None


class HistogramRequest(CamelModel):
    """Specification of a histogram request in Zeno.

    Attributes:
        columns (list[ZenoColumn]): the columns to calculate histograms for.
        filter_predicates (FilterPredicateGroup | None): the filter predicates to be
            applied to the data.
        model (str | None): the model to be used for the histogram.
        metric (Metric | None): the metric to be used for the histogram.
        data_ids (list[str] | None): the data ids to be used for the histogram.
    """

    columns: list[ZenoColumn]
    filter_predicates: FilterPredicateGroup | None = None
    model: str | None = None
    metric: Metric | None = None
    data_ids: list[str] | None = None


class StringFilterRequest(CamelModel):
    """Specification of a string filter request in Zeno.

    Attributes:
        column (ZenoColumn): the column to be used for the filter.
        filter_string (str): the string to be used for the filter.
        operation (Operation): the operation to be used for the filter.
    """

    column: ZenoColumn
    filter_string: str
    operation: Operation
