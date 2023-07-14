"""Functions to select data from the database."""
from typing import List, Optional

from connex.classes.endpoint import Endpoint
from connex.classes.project import Project
from connex.database.database import Database


def select_secret(email: str) -> Optional[str]:
    """Get the secret of a user with a specific email address.

    Args:
        email (str): the email address of the user for which to fetch the secret.

    Returns:
        Optional[str]: the secret of the user.
    """
    db = Database()
    secret = db.connect_execute_return(
        "SELECT secret FROM account WHERE email = %s", [email]
    )
    if secret is None:
        return None
    return str(secret[0])


def select_endpoints() -> List[Endpoint]:
    """Get all endpoints that are available to the user.

    Returns:
        List[Endpoint]: the list of all available endpoints.
    """
    db = Database()
    endpoints_result = db.connect_execute_return(
        "SELECT * FROM endpoint", return_all=True
    )
    endpoints: List[Endpoint] = []
    if endpoints_result is not None:
        for endpoint in endpoints_result:
            endpoints.append(
                Endpoint(id=endpoint[0], name=endpoint[1], url=endpoint[2])
            )
    return endpoints


def select_all_projects() -> List[Project]:
    """Get all projects available to the user.

    Returns:
        List[Project]: list of all available projects.
    """
    db = Database()
    project_results = db.connect_execute_return(
        "SELECT project.uuid, project.name, endpoint.id, endpoint.url FROM project "
        "INNER JOIN endpoint ON endpoint.id = project.endpoint_id",
        return_all=True,
    )
    projects: List[Project] = []
    if project_results is not None:
        for project in project_results:
            projects.append(
                Project(
                    uuid=project[0],
                    name=project[1],
                    endpoint_id=project[2],
                    url=project[3],
                )
            )
    return projects


def select_project(uuid: str) -> Project:
    """Get a project by its uuid.

    Args:
        uuid (str): the uuid of the project to fetch.

    Returns:
        Project: the project with the requested UUID.
    """
    db = Database()
    project_results = db.connect_execute_return(
        "SELECT project.uuid, project.name, endpoint.id, endpoint.url FROM project "
        "INNER JOIN endpoint ON endpoint.id = project.endpoint_id "
        "WHERE project.uuid = %s",
        [uuid],
    )
    return (
        Project(
            uuid=str(project_results[0]),
            name=str(project_results[1]),
            endpoint_id=project_results[2]
            if isinstance(project_results[2], int)
            else 0,
            url=str(project_results[3]),
        )
        if project_results is not None
        else Project(uuid="", name="", endpoint_id=0, url="")
    )
