"""Type representations for table data."""
from typing import List, Optional, Tuple, Union

from zeno_backend.classes.base import CamelModel, ZenoColumn
from zeno_backend.classes.slice import FilterPredicateGroup


class TableRequest(CamelModel):
    """A request specification for table data."""

    columns: List[ZenoColumn]
    diff_column_1: Optional[ZenoColumn] = None
    diff_column_2: Optional[ZenoColumn] = None
    offset: int
    limit: int
    filter_predicates: Optional[FilterPredicateGroup] = None
    sort: Tuple[Union[ZenoColumn, str, None], bool]
    data_ids: Optional[List[str]] = None
