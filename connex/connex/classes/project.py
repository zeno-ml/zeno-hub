"""Types for Connex's projects."""
from typing import Optional

from connex.classes.base import CamelModel


class Project(CamelModel):
    """Representation for a project in Connex."""

    uuid: str
    name: str
    endpoint_id: int
    url: Optional[str]
