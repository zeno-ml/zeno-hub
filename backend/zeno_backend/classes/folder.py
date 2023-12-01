"""Type representation for folder data."""
from zeno_backend.classes.base import CamelModel


class Folder(CamelModel):
    """Specification of a folder in Zeno.

    Attributes:
        id (int): the id of the folder.
        name (str): the name of the folder.
        project_uuid (str | None): the uuid of the project the folder belongs to.
    """

    id: int
    name: str
    project_uuid: str | None = None
