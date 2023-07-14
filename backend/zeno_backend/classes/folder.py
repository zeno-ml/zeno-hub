"""Type representation for folder data."""
from zeno_backend.classes.base import CamelModel


class Folder(CamelModel):
    """Specification of a folder in Zeno."""

    id: int
    name: str
