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
    """

    id: int
    slice_name: str
    folder_id: int | None = None
    filter_predicates: FilterPredicateGroup
