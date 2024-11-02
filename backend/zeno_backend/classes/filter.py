"""Classes required for specifying data filters."""

import json
from enum import Enum
from typing import LiteralString

from pydantic import StrictBool, StrictFloat, StrictInt, StrictStr

from zeno_backend.classes.base import CamelModel, ZenoColumn


class Operation(str, Enum):
    """Enumeration of possible filter operations.

    Attributes:
        EQUAL: equal to.
        DIFFERENT: different from.
        GT: greater than.
        LT: less than.
        LTE: less than or equal to.
        GTE: greater than or equal to.
        LIKE: like.
        ILIKE: ilike.
        REGEX: regex.
        NOT_REGEX: not matching regex.
    """

    EQUAL = "EQUAL"
    DIFFERENT = "DIFFERENT"
    GT = "GT"
    LT = "LT"
    LTE = "LTE"
    GTE = "GTE"
    LIKE = "LIKE"
    ILIKE = "ILIKE"
    REGEX = "REGEX"
    NOT_REGEX = "NOT_REGEX"

    def literal(self) -> LiteralString:
        """Obtain a string representation to be used in a SQL filter.

        Returns:
            str: SQL filter string for an operation.
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
        if self == Operation.ILIKE:
            return "ILIKE"
        if self == Operation.REGEX:
            return "~"
        if self == Operation.NOT_REGEX:
            return "!~"
        return "LIKE"


class Join(str, Enum):
    """Enumeration of the join operators between filter predicates.

    Attributes:
        AND: logical AND.
        OR: logical OR.
        OMITTED: no join.
    """

    AND = "AND"
    OR = "OR"
    OMITTED = " "


class FilterPredicate(CamelModel):
    """Predicates to specify a filter operation on a column of the data table.

    Attributes:
        column (ZenoColumn): column to be filtered.
        operation (Operation): operation to be applied.
        value (StrictStr | StrictBool | StrictInt | StrictFloat): value to filter with.
        join (Join): join operator to be used.
    """

    column: ZenoColumn
    operation: Operation
    value: StrictStr | StrictBool | StrictInt | StrictFloat
    join: Join


class FilterPredicateGroup(CamelModel):
    """Group of filter predicates that might be joined by a Join operator.

    Attributes:
        predicates (list[FilterPredicateGroup | FilterPredicate]): predicates to be
            applied for the filter.
        join (Join): join operator to be used between groups.
    """

    predicates: list["FilterPredicateGroup | FilterPredicate"]
    join: Join


class PredicatesEncoder(json.JSONEncoder):
    """Encoding a predicate group as json data."""

    def default(self, o: FilterPredicateGroup):
        """Transform a FilterPredicateGroup into JSON data to be saved in a SQL table.

        Args:
            o (FilterPredicateGroup): predicates to be converted.

        Returns:
            dict: a dictionary representation that can be parsed by a JSON encoder.
        """
        return o.__dict__
