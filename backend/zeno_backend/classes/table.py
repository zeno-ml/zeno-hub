"""Type representations for table data."""

from zeno_backend.classes.base import CamelModel, ZenoColumn
from zeno_backend.classes.slice import FilterPredicateGroup


class TableRequest(CamelModel):
    """A request specification for table data."""

    columns: list[ZenoColumn]
    model: str | None = None
    diff_column_1: ZenoColumn | None = None
    diff_column_2: ZenoColumn | None = None
    offset: int
    limit: int
    filter_predicates: FilterPredicateGroup | None = None
    sort: tuple[ZenoColumn | None, bool]
    data_ids: list[str] | None = None
