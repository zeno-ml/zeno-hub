"""FastAPI server endpoints for user and organization related queries."""
from amplitude import BaseEvent
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

import zeno_backend.database.delete as delete
import zeno_backend.database.insert as insert
import zeno_backend.database.select as select
import zeno_backend.database.update as update
import zeno_backend.util as util
from zeno_backend.classes.amplitude import AmplitudeHandler
from zeno_backend.classes.user import Organization, User

router = APIRouter(tags=["zeno"])


@router.post(
    "/login",
    response_model=User,
    tags=["zeno"],
)
async def login(name: str, current_user=Depends(util.auth.claim())):
    """Log a user in to Zeno.

    Args:
        name (str): name of the user to be logged in.
        current_user (Any, optional): user making the login request.
            Defaults to Depends(util.auth.claim()).

    Raises:
        HTTPException: error if the login failed.

    Returns:
        User: user that has been logged in.
    """
    try:
        fetched_user = await select.user(name)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
    if fetched_user is None:
        try:
            user = User(id=-1, name=name, admin=None, cognito_id=current_user["sub"])
            await insert.user(user)
            await insert.api_key(user)
            AmplitudeHandler().track(
                BaseEvent(
                    event_type="Signup",
                    user_id=user.cognito_id,
                )
            )
            return await select.user(name)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(exc),
            ) from exc

    if fetched_user.cognito_id is None:
        try:
            await update.user(
                User(id=fetched_user.id, name=name, cognito_id=current_user["sub"])
            )
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(exc),
            ) from exc

    return fetched_user


@router.get(
    "/users",
    response_model=list[User],
    tags=["zeno"],
    dependencies=[Depends(util.auth)],
)
async def get_users():
    """Get all users in the database.

    Returns:
        list[User]: list of all users.
    """
    return await select.users()


@router.get(
    "/organizations",
    response_model=list[Organization],
    tags=["zeno"],
    dependencies=[Depends(util.auth)],
)
async def get_organizations():
    """Get all organizations in the database.

    Returns:
        list[Organization]: list of all organizations.
    """
    return await select.organizations()


@router.post("/user_organizations", tags=["zeno"], response_model=list[Organization])
async def get_user_organizations(current_user=Depends(util.auth.claim())):
    """Get all organizations a specified user is a member of.

    Args:
        current_user (Any, optional): user making the request.
            Defaults to Depends(util.auth.claim()).

    Raises:
        HTTPException: error if the user is not found.

    Returns:
        list[Organization]: all organizations the user is a member of.
    """
    user = await select.user(current_user["username"])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User not found",
        )
    return await select.user_organizations(user)


@router.post(
    "/api-key/",
    response_model=str,
    tags=["zeno"],
    dependencies=[Depends(util.auth)],
)
async def create_api_key(current_user=Depends(util.auth.claim())):
    """Create a new API key for a specific user.

    Args:
        current_user (Any, optional): user making the API key request.
            Defaults to Depends(util.auth.claim()).

    Returns:
        str | None: new API key of the user.
    """
    user = await select.user(current_user["username"])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User not found",
        )
    return await insert.api_key(user)


@router.post("/organization", tags=["zeno"], dependencies=[Depends(util.auth)])
async def add_organization(user: User, organization: Organization):
    """Add an organization to the database.

    Args:
        user (User): user creating the new organization.
        organization (Organization): specification of the organization to be created.
    """
    await insert.organization(user, organization)


@router.patch("/user/", tags=["zeno"], dependencies=[Depends(util.auth)])
async def update_user(user: User):
    """Update a user's profile.

    Args:
        user (User): updated user profile.
    """
    await update.user(user)


@router.patch("/organization/", tags=["zeno"], dependencies=[Depends(util.auth)])
async def update_organization(organization: Organization):
    """Update an organization in the database.

    Args:
        organization (Organization): updated organization.
    """
    await update.organization(organization)


@router.delete("/organization", tags=["zeno"], dependencies=[Depends(util.auth)])
async def delete_organization(organization: Organization):
    """Delete an organization from the database.

    Args:
        organization (Organization): organization to be deleted.
    """
    await delete.organization(organization)
