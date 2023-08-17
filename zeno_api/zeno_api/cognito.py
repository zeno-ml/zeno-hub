"""Handle cognito functionality for authentication."""
import os
from pathlib import Path

from dotenv import load_dotenv
from pycognito import Cognito


def get_user(username: str, password: str):
    """Sets the access token from cognito for a certain user to an environment variable.

    Args:
        username (str): the username for which to get the access token.
        password (str): the password used by the user to login.
    """
    # load env vars for cognito if available
    env_path = Path("../frontend/.env")
    if env_path.exists():
        load_dotenv(env_path)

    # function to get the user from cognito
    user = Cognito(
        os.environ["ZENO_USER_POOL_ID"],
        os.environ["ZENO_USER_POOL_CLIENT_ID"],
        username=username,
    )
    user.authenticate(password=password)
    return user
