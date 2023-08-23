"""Types for Zeno's users."""

from zeno_backend.classes.base import CamelModel


class User(CamelModel):
    """Representation of a user in Zeno."""

    id: int
    name: str
    admin: bool | None = None


class Organization(CamelModel):
    """Representation of a organization in Zeno."""

    id: int
    name: str
    members: list[User]
    admin: bool
