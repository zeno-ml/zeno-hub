"""Classes for the Zeno SDK."""
from zeno_backend.classes.base import CamelModel


class DatasetSchema(CamelModel):
    """Metadata for dataset columns.

    Attributes:
        project_uuid (str): unique identifier of the project.
        columns (list[str]): list of column names.
        id_column (str): column name of the unique identifier.
        data_column (str): column name of the input data instance.
        label_column (str): column name of the ground truth label.
    """

    project_uuid: str
    columns: list[str]
    id_column: str
    data_column: str = ""
    label_column: str = ""


class SystemSchema(CamelModel):
    """Metadata for system columns.

    Attributes:
        project_uuid (str): unique identifier of the project.
        system_name (str): name of the system.
        columns (list[str]): list of column names.
        id_column (str): column name of the unique identifier.
        output_column (str): column name of the system output.
    """

    project_uuid: str
    system_name: str
    columns: list[str]
    id_column: str
    output_column: str
