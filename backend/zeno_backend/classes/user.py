"""Types for Zeno's users."""
from typing import Optional

from zeno_backend.classes.base import CamelModel


class User(CamelModel):
    """Representation of a user in Zeno."""

    name: Optional[str]
    email: str
    secret: Optional[str]
