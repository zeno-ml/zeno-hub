"""Type representations for tags."""
from typing import List, Optional

from zeno_backend.classes.base import CamelModel
from zeno_backend.classes.metric import Metric


class Tag(CamelModel):
    """Specification of the tag type in Zeno.

    Attributes:
        id (int): The id of the tag.
        tag_name (str): The name of the tag.
        data_ids (List[str]): The ids of the data belonging to the tag.
        folder_id (Optiona[int]): The id of the folder the tag belongs to. Default None.
    """

    id: int
    tag_name: str
    data_ids: List[str]
    folder_id: Optional[int] = None


class TagMetricKey(CamelModel):
    """Specification of TagMetricKeys in Zeno.

    TagMetricKeys can be used to calculate metrics for specific tags.

    Attributes:
        tag (Tag): The tag to calculate metrics for.
        model (str): The model to calculate metrics for.
        metric (Metric): The metric to calculate.
    """

    tag: Tag
    model: str
    metric: Metric
