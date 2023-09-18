"""Type representation for folder data."""
from zeno_backend.classes.base import CamelModel


class Folder(CamelModel):
    """Specification of a folder in Zeno.

    Attributes:
        id (int): the id of the folder.
        name (str): the name of the folder.
    """

    id: int
    name: str
