"""Types for Zeno's users."""

from zeno_backend.classes.base import CamelModel


class User(CamelModel):
    """Representation of a user in Zeno.

    Attributes:
        id (int): ID of the user.
        name (str): name of the user.
        display_name (str): display name of the user.
        cognito_id (str | None): Cognito ID of the user. Default None.
        admin (bool | None): whether the user is an admin. Default None.
    """

    id: int
    name: str
    display_name: str
    cognito_id: str | None = None
    admin: bool | None = None


class Organization(CamelModel):
    """Representation of a organization in Zeno.

    Attributes:
        id (int): ID of the organization.
        name (str): name of the organization.
        members (list[User]): members of the organization.
        admin (bool): whether the current user is an admin of the organization.
    """

    id: int
    name: str
    members: list[User]
    admin: bool


class Author(CamelModel):
    """Zeno report author for displaying author list.

    Attributes:
        user (User): User object for author.
        position (int): position of the author in the list of authors.
    """

    user: User
    position: int
