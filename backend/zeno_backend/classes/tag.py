"""Type representations for tags."""

from zeno_backend.classes.base import CamelModel


class Tag(CamelModel):
    """Specification of the tag type in Zeno.

    Attributes:
        id (int): The id of the tag.
        tag_name (str): The name of the tag.
        data_ids (list[str]): The ids of the data belonging to the tag.
        folder_id (Optiona[int]): The id of the folder the tag belongs to. Default None.
    """

    id: int
    tag_name: str
    data_ids: list[str]
    folder_id: int | None = None


class TagMetricKey(CamelModel):
    """Specification of TagMetricKeys in Zeno.

    TagMetricKeys can be used to calculate metrics for specific tags.

    Attributes:
        tag (Tag): The tag to calculate metrics for.
        model (str | None): The model to calculate metrics for.
        metric (int | None): The metric to calculate.
    """

    tag: Tag
    model: str | None = None
    metric: int | None = None
