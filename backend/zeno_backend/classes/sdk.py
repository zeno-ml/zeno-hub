from zeno_backend.classes.base import CamelModel


class DatasetSchema(CamelModel):
    """Metadata for dataset columns.

    Attributes:
        project_uuid (str): unique identifier of the project.
        columns (list[str]): list of column names.
        id_column (str): column name of the unique identifier.
        label_column (str): column name of the ground truth label.
        data_column (str): column name of the raw input data instance.
        url_column (str): column name of the link to the input data instance.
    """

    project_uuid: str
    columns: list[str]
    id_column: str
    label_column: str = ""
    data_column: str = ""
    url_column: str = ""
