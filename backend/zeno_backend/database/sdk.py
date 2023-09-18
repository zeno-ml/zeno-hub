from zeno_backend.classes.base import CamelModel


class DatasetInfo(CamelModel):
    """Dataset information.

    Attributes:
        id_column (str): name of the column containing the ID.
        label_column (str): name of the column containing the label.
    data_column (str): name of the column containing the data.
    """

    id_column: str
    label_column: str
    data_column: str
