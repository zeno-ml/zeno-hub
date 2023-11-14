"""Type representations for table data."""

from zeno_backend.classes.base import CamelModel, ZenoColumn
from zeno_backend.classes.slice import FilterPredicateGroup


class TableRequest(CamelModel):
    """A request specification for table data.

    Attributes:
        columns (list[ZenoColumn]): the columns to be used for the table.
        model (str | None): the model to be used for the table.
        diff_column_1 (ZenoColumn | None): the first diff column to be used for the
            table.
        diff_column_2 (ZenoColumn | None): the second diff column to be used for the
            table.
        offset (int): the offset to be used for the table.
        limit (int): the limit to be used for the table.
        filter_predicates (FilterPredicateGroup | None): the filter predicates to be
            applied to the data.
        sort (tuple[ZenoColumn | None, bool]): the sort to be used for the table.
        data_ids (list[str] | None): the data ids to be used for the table.
    """

    columns: list[ZenoColumn]
    model: str | None = None
    diff_column_1: ZenoColumn | None = None
    diff_column_2: ZenoColumn | None = None
    offset: int
    limit: int
    filter_predicates: FilterPredicateGroup | None = None
    sort: tuple[ZenoColumn | None, bool]
    data_ids: list[str] | None = None


class SliceTableRequest(CamelModel):
    """Request for a slice of a table for Report view."""

    slice_id: int
    model: str | None = None
    offset: int
    limit: int


class TagTableRequest(CamelModel):
    """Request for a table for a given Tag in Report view."""

    tag_id: int
    model: str | None = None
    offset: int
    limit: int
