"""Type representation for slice data."""

from zeno_backend.classes.base import CamelModel
from zeno_backend.classes.filter import FilterPredicateGroup


class Slice(CamelModel):
    """Specification of a slice in Zeno."""

    id: int
    slice_name: str
    folder_id: int | None = None
    filter_predicates: FilterPredicateGroup
