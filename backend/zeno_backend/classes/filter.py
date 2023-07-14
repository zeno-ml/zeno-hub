"""Classes required for specifying data filters."""
import json
from enum import Enum
from typing import List, LiteralString, Union

from zeno_backend.classes.base import CamelModel, ZenoColumn


class Operation(str, Enum):
    """Enumeration of possible filter operations."""

    EQUAL = "EQUAL"
    DIFFERENT = "DIFFERENT"
    GT = "GT"
    LT = "LT"
    LTE = "LTE"
    GTE = "GTE"
    LIKE = "LIKE"

    def literal(self) -> LiteralString:
        """Obtain a string representation to be used in a SQL filter.

        Returns:
            str: the SQL filter string for an operation.
        """
        if self == Operation.EQUAL:
            return "="
        if self == Operation.DIFFERENT:
            return "!="
        if self == Operation.GT:
            return ">"
        if self == Operation.LT:
            return "<"
        if self == Operation.GTE:
            return ">="
        if self == Operation.LTE:
            return "<="
        return "LIKE"


class Join(str, Enum):
    """Enumeration of the join operators between filter predicates."""

    AND = "AND"
    OR = "OR"
    OMITTED = " "


class FilterPredicate(CamelModel):
    """Predicates to specify a filter operation on a column of the data table."""

    column: ZenoColumn
    operation: Operation
    value: Union[str, float, int, bool]
    join: Join


class FilterPredicateGroup(CamelModel):
    """Group of filter predicates that might be joined by a Join operator."""

    predicates: List[Union["FilterPredicateGroup", FilterPredicate]]
    join: Join


class PredicatesEncoder(json.JSONEncoder):
    """Encoding a predicate group as json data."""

    def default(self, o: FilterPredicateGroup):
        """Transform a FilterPredicateGroup into JSON data to be saved in a SQL table.

        Args:
            o (FilterPredicateGroup): The predicates to be converted.

        Returns:
            dict: a dictionary representation that can be parsed by a JSON encoder.
        """
        return o.__dict__
