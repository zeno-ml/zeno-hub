"""Types for Zeno's users."""
from typing import List, Optional

from zeno_backend.classes.base import CamelModel


class User(CamelModel):
    """Representation of a user in Zeno."""

    id: int
    name: str
    admin: Optional[bool] = None


class Organization(CamelModel):
    """Representation of a organization in Zeno."""

    id: int
    name: str
    members: List[User]
    admin: bool
