"""Utility functions for Zeno's backend."""
import os

import cognitojwt
from fastapi import HTTPException, Request, status
from fastapi_cloudauth.cognito import Cognito

from zeno_backend import util
from zeno_backend.classes.user import User
from zeno_backend.database import select

# function to get the user from cognito
auth = Cognito(
    region=os.environ["ZENO_USER_POOL_AUTH_REGION"],
    userPoolId=os.environ["ZENO_USER_POOL_ID"],
    client_id=os.environ["ZENO_USER_POOL_CLIENT_ID"],
)


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


async def project_access_valid(project: str | None, request: Request):
    """Check whether accessing a resource is valid.

    Args:
        project (str | None): the project for which to access a resource.
        request (Request): the request to get the access token if needed.

    Throws:
        HTTPException: if the project is not found or access is not valid.
    """
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    if not await select.project_public(project):
        token = request.headers.get("authorization")
        user = await util.get_user_from_token(request)
        if token is None or not verify_token(token) or user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )
        available_project_ids = [x.uuid for x in await select.projects(user)]
        if project not in available_project_ids:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )


async def project_editor(project_uuid: str, request: Request):
    """Check whether a user is an editor of a project.

    Args:
        project_uuid (str): the project to check.
        request (Request): the request to get the access token if needed.

    Throws:
        HTTPException: if the project is not found or the user is not an editor.
    """
    token = request.headers.get("authorization")
    user = await util.get_user_from_token(request)
    if token is None or not verify_token(token) or user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    available_project_ids = [
        project.uuid for project in await select.projects(user) if project.editor
    ]
    if project_uuid not in available_project_ids:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )


async def report_access_valid(report: int, request: Request):
    """Check whether accessing a resource is valid.

    Args:
        report (int): the report for which to access a resource.
        request (Request): the request to get the access token if needed.

    Returns:
        bool: whether or not othe project data can be accessed.
    """
    if not await select.report_public(report):
        token = request.headers.get("authorization")
        user = await util.get_user_from_token(request)
        if token is None or not verify_token(token) or user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )
        available_report_ids = [x.id for x in await select.reports(user)]
        if report not in available_report_ids:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )


async def report_editor(report_id: int, request: Request):
    """Check whether a user is an editor of a report.

    Args:
        report_id (int): the report to check.
        request (Request): the request to get the access token if needed.

    Throws:
        HTTPException: if the report is not found or the user is not an editor.
    """
    token = request.headers.get("authorization")
    user = await util.get_user_from_token(request)
    if token is None or not verify_token(token) or user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    available_report_ids = [
        report.id for report in await select.reports(user) if report.editor
    ]
    if report_id not in available_report_ids:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )


async def get_user_from_token(request: Request) -> User | None:
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
        return await select.user(user_dict["username"])
    except cognitojwt.CognitoJWTException:
        return None
