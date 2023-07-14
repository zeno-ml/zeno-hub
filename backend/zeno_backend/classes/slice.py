"""Type representation for slice data."""
from typing import Optional

from zeno_backend.classes.base import CamelModel
from zeno_backend.classes.filter import FilterPredicateGroup


class Slice(CamelModel):
    """Specification of a slice in Zeno."""

    id: int
    slice_name: str
    folder_id: Optional[int]
    filter_predicates: FilterPredicateGroup
