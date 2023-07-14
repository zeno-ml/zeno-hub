"""Types for Connex's backend endpoints."""
from typing import Optional

from connex.classes.base import CamelModel


class Endpoint(CamelModel):
    """Representation of a backend endpoint in Connex."""

    id: Optional[int]
    name: str
    url: str
