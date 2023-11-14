"""Type representations for tags."""

from zeno_backend.classes.base import CamelModel


class Tag(CamelModel):
    """Specification of the tag type in Zeno.

    Attributes:
        id (int): id of the tag.
        tag_name (str): name of the tag.
        data_ids (list[str]): ids of the data belonging to the tag.
        folder_id (Optiona[int]): id of the folder the tag belongs to. Default None.
        project_uuid (Optional[str]): uuid of the project the tag belongs to.
    """

    id: int
    tag_name: str
    data_ids: list[str]
    folder_id: int | None = None
    project_uuid: str | None = None


class TagMetricKey(CamelModel):
    """Specification of TagMetricKeys in Zeno.

    TagMetricKeys can be used to calculate metrics for specific tags.

    Attributes:
        tag (Tag): tag to calculate metrics for.
        model (str | None): model to calculate metrics for.
        metric (int | None): metric to calculate.
    """

    tag: Tag
    model: str | None = None
    metric: int | None = None
