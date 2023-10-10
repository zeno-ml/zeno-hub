"""Type representation for slice data."""

from zeno_backend.classes.base import CamelModel
from zeno_backend.classes.filter import FilterPredicateGroup


class Slice(CamelModel):
    """Specification of a slice in Zeno.

    Attributes:
        id (int): the id of the slice.
        slice_name (str): the name of the slice.
        folder_id (int | None): the id of the folder the slice belongs to.
        filter_predicates (FilterPredicateGroup): the filter predicates of the slice.
        project_uuid (str | None): the uuid of the project the slice belongs to.
    """

    id: int
    slice_name: str
    filter_predicates: FilterPredicateGroup
    folder_id: int | None = None
    project_uuid: str | None = None
