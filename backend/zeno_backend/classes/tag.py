"""Type representations for tags."""
from typing import List, Optional

from zeno_backend.classes.base import CamelModel
from zeno_backend.classes.metric import Metric


class Tag(CamelModel):
    """Specification of the tag type in Zeno."""

    id: int
    tag_name: str
    folder_id: Optional[int]
    items: List[str]


class TagMetricKey(CamelModel):
    """Specification of TagMetricKeys in Zeno.

    TagMetricKeys can be used to calculate metrics for specific tags.
    """

    tag: Tag
    model: str
    metric: Metric
