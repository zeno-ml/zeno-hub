"""Type representations for metric data."""
from zeno_backend.classes.base import CamelModel
from zeno_backend.classes.slice import Slice


class Metric(CamelModel):
    """Specification for a metric in a Zeno project.

    Attributes:
        id (int): the id of the metric to be used.
        name (str): The name of the metric.
        type (str): The type of metric to calculate.
        columns (list[str]): The columns to calculate the metric on.
    """

    id: int
    name: str
    type: str
    columns: list[str]

    def __hash__(self):
        """Hash representation of metric, based on id since guaranteed unique.

        Returns:
            int: the hash of the metric.
        """
        return self.id


class MetricKey(CamelModel):
    """Specification of metric keys in zeno.

    Metric keys map to a specific slice, model, and metric.

    Attributes:
        slice (Slice): the slice to be used for the metric.
        model (str): the model to be used for the metric.
        metric (int): the metric to be used for the metric.
    """

    slice: Slice
    model: str
    metric: int


class MetricRequest(CamelModel):
    """Specification of a metric request in Zeno.

    Can be used to request metric calculation on specific data subsets.

    Attributes:
        metric_keys (list[MetricKey]): the metric keys to be used for the metric.
        data_ids (list[str] | None): the data ids to be used for the metric.
    """

    metric_keys: list[MetricKey]
    data_ids: list[str] | None = None
