"""Base types used in Zeno's backend."""
from enum import Enum
from typing import Any, Optional, Union

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


class ProjectConfig(CamelModel):
    """Configuration specification of the Zeno project."""

    uuid: str
    name: str
    view: str
    calculate_histogram_metrics: bool = True
    num_items: int = 10
    editor: bool
    public: bool


class ZenoColumnType(str, Enum):
    """Enumeration of possible column types in Zeno."""

    ITEM = "ITEM"
    LABEL = "LABEL"
    METADATA = "METADATA"
    PREDISTILL = "PREDISTILL"
    OUTPUT = "OUTPUT"
    EMBEDDING = "EMBEDDING"
    POSTDISTILL = "POSTDISTILL"


class MetadataType(str, Enum):
    """Enumeration of possible metadata types in Zeno."""

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
    """Representation of a column in Zeno's project data."""

    id: str
    column_type: ZenoColumnType
    name: str
    data_type: MetadataType
    model: Optional[str] = None


class LabelSpec(CamelModel):
    """Specification for a label in Zeno's project data."""

    item: str
    label: str


class OutputSpec(CamelModel):
    """Specification for a model output in Zeno's project data."""

    item: str
    output: str
    model: str


class PredistillSpec(CamelModel):
    """Specification for predistill metadata in Zeno."""

    col_name: str
    value: Any = None
    item: str
    type: MetadataType


class PostdistillSpec(CamelModel):
    """Specification for postdistill data in Zeno."""

    col_name: str
    value: Any = None
    item: str
    type: MetadataType
    model: str


class GroupMetric(CamelModel):
    """Specification for a metric on a group of items."""

    metric: Union[float, None] = None
    size: int
