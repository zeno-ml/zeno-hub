"""Base types used in Zeno's backend."""
from enum import Enum

from pydantic import BaseModel, ConfigDict


def to_camel(string: str) -> str:
    """Converter for variables from snake_case to camelCase.

    Args:
        string (str): the variable to convert to camelCase.

    Returns:
        str: camelCase representation of the variable.
    """
    components = string.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class CamelModel(BaseModel):
    """Converting snake_case pydantic models to camelCase models."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ZenoColumnType(str, Enum):
    """Enumeration of possible column types in Zeno.

    Attributes:
        ID: unique identifier.
        DATA: raw input data instance.
        DATA_URL: link to input data instance.
        LABEL: ground truth label.
        OUTPUT: model output.
        FEATURE: metadata feature for data instance.
        EMBEDDING: vector embedding representing a data instance or output.
    """

    ID = "ID"
    DATA = "DATA"
    DATA_URL = "DATA_URL"
    LABEL = "LABEL"
    OUTPUT = "OUTPUT"
    FEATURE = "FEATURE"
    EMBEDDING = "EMBEDDING"


class MetadataType(str, Enum):
    """Enumeration of possible metadata types in Zeno.

    Attributes:
        NOMINAL: nominal metadata type, e.g. string or small cardinality number.
        CONTINUOUS: continuous metadata type, e.g. large cardinality number.
        BOOLEAN: boolean metadata type, e.g. True or False.
        DATETIME: datetime metadata type, e.g. 2021-01-01 00:00:00.
        OTHER: any other metadata type, e.g. strings.
    """

    NOMINAL = "NOMINAL"
    CONTINUOUS = "CONTINUOUS"
    BOOLEAN = "BOOLEAN"
    DATETIME = "DATETIME"
    OTHER = "OTHER"

    def __str__(self) -> str:
        """Get a SQL representation for a metadata type.

        Returns:
            str: the sql data type corresponding to the metadata type.
        """
        if self == MetadataType.BOOLEAN:
            return "BOOLEAN"
        if self == MetadataType.CONTINUOUS:
            return "NUMERIC"
        if self == MetadataType.DATETIME:
            return "DATETIME"
        return "TEXT"


class ZenoColumn(CamelModel):
    """Representation of a column in a Zeno project.

    Attributes:
        id (str): ID of the column.
        name (str): name of the column.
        column_type (ZenoColumnType): type of the column.
        data_type (MetadataType): data type of the column.
        model (str | None): name of the model that produced the column.
    """

    id: str
    name: str
    column_type: ZenoColumnType
    data_type: MetadataType
    model: str | None = None


class GroupMetric(CamelModel):
    """Specification for a metric on a group of datapoints."""

    metric: float | None = None
    size: int
