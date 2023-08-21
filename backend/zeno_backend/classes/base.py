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


class ZenoColumnType(str, Enum):
    """Enumeration of possible column types in Zeno.

    Attributes:
        DATA: Input data instance. Either raw data or filename.
        LABEL: Ground truth label.
        OUTPUT: Model output.
        FEATURE: Metadata feature for an input data instance.
        EMBEDDING: Vector embedding representing a data instance or output.
    """

    DATA = "DATA"
    LABEL = "LABEL"
    OUTPUT = "OUTPUT"
    FEATURE = "FEATURE"
    EMBEDDING = "EMBEDDING"


class MetadataType(str, Enum):
    """Enumeration of possible metadata types in Zeno.

    Attributes:
        NOMINAL: Nominal metadata type, e.g. string or small cardinality number.
        CONTINUOUS: Continuous metadata type, e.g. large cardinality number.
        BOOLEAN: Boolean metadata type, e.g. True or False.
        DATETIME: Datetime metadata type, e.g. 2021-01-01 00:00:00.
        OTHER: Any other metadata type, e.g. strings.
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


class Project(CamelModel):
    """Projects with datasets & models.

    Attributes:
        uuid (str): The UUID of the task.
        name (str): The name of the task.
        view (str): The name of the view to use for the task.
        data_url (str): The base URL from which to read data instances.
        editor (bool): Whether the current user is an editor of the project.
        calculate_histogram_metrics (bool): Whether to calculate histogram metrics.
            Default True.
        samples_per_page (int): The number of items to show per page. Default 10.
        public (bool): Whether the task is public. Default False.
    """

    uuid: str
    name: str
    view: str
    data_url: str
    editor: bool
    calculate_histogram_metrics: bool = True
    samples_per_page: int = 10
    public: bool = False


class ProjectStats(CamelModel):
    """Statistical numbers of a Zeno project.

    Attributes:
        num_instances (int): number of data instances in the project.
        num_charts (int): number of charts that have been created for the project.
        num_models (int): number of models associated with the project
    """

    num_instances: int
    num_charts: int
    num_models: int


class ZenoColumn(CamelModel):
    """Representation of a column in a Zeno project.

    Attributes:
        id (str): The ID of the column.
        name (str): The name of the column.
        column_type (ZenoColumnType): The type of the column.
        data_type (MetadataType): The data type of the column.
        model (Optional[str]): The name of the model that produced the column.
    """

    id: str
    name: str
    column_type: ZenoColumnType
    data_type: MetadataType
    model: Optional[str] = None


class LabelSpec(CamelModel):
    """Specification for a label in a Zeno project.

    Attributes:
        data_id (str): The ID of the associated data instance.
        label (str): The ground truth label for the data instance.
    """

    data_id: str
    label: str


class OutputSpec(CamelModel):
    """Specification for a model output in a Zeno project.

    Attributes:
        data_id (str): The ID of the associated data instance.
        model (str): The name of the model that produced the output.
        output (str): The model's output for the data instance.
    """

    data_id: str
    model: str
    output: str


class FeatureSpec(CamelModel):
    """Specification for a metadata feature in a Zeno project.

    Attributes:
        data_id (str): The ID of the associated data instance.
        col_name (str): The name of the associated column.
        type (MetadataType): The type of the metadata feature.
        value (Any): The value of the metadata feature. Default None.
        model (Optional[str]): The name of the model associated with the
            metadata feature.
    """

    data_id: str
    col_name: str
    type: MetadataType
    value: Any = None
    model: Optional[str] = None


class GroupMetric(CamelModel):
    """Specification for a metric on a group of items."""

    metric: Union[float, None] = None
    size: int
