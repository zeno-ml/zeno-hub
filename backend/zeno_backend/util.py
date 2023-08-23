"""Utility functions for Zeno's backend."""
import os

import cognitojwt
from fastapi import Request

from zeno_backend.classes.user import User
from zeno_backend.database import select


def verify_token(token: str) -> bool:
    """Verify a cognito access token.

    Args:
        token (str): the token to be verified.

    Returns:
        bool: whether or not verification succeeded.
    """
    try:
        cognitojwt.decode(
            token.split(" ")[1],
            os.environ["ZENO_USER_POOL_AUTH_REGION"],
            os.environ["ZENO_USER_POOL_ID"],
            os.environ["ZENO_USER_POOL_CLIENT_ID"],
        )
        return True
    except cognitojwt.CognitoJWTException:
        return False


def access_valid(project: str, request: Request) -> bool:
    """Check whether accessing a resource is valid.

    Args:
        project (str): the project for which to access a resource.
        public (bool): whether the project is public.
        request (Request): the request to get the access token if needed.

    Returns:
        bool: whether or not othe project data can be accessed.
    """
    if not is_project_public(project):
        token = request.headers.get("authorization")
        if token is None or not verify_token(token):
            return False
    return True


def get_user_from_token(request: Request) -> User | None:
    """Get a user from a cognito access token.

    Args:
        request (Request): the request containing access token.

    Returns:
        User | None: the user associated with the token.
    """
    token = request.headers.get("authorization")
    if token is None:
        return None
    try:
        user_dict = cognitojwt.decode(
            token.split(" ")[1],
            os.environ["ZENO_USER_POOL_AUTH_REGION"],
            os.environ["ZENO_USER_POOL_ID"],
            os.environ["ZENO_USER_POOL_CLIENT_ID"],
        )
        return select.user((user_dict["username"]))
    except cognitojwt.CognitoJWTException:
        return None
