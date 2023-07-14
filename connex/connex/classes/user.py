"""Types for Connex's users."""
from typing import Optional

from connex.classes.base import CamelModel


class User(CamelModel):
    """Representation of a user in Connex."""

    name: Optional[str]
    email: str
    secret: Optional[str]
