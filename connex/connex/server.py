"""The FastAPI server for the Connex. Provides endpoints to login and load projects."""
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, status

import connex.database.insert as insert
import connex.database.select as select
from connex.classes.endpoint import Endpoint
from connex.classes.project import Project
from connex.classes.user import User


def get_server() -> FastAPI:
    """Provide the FastAPI server and specifies its inputs.

    Raises:
    ------
        HTTPException: Something goes wrong server-side.

    Returns:
    -------
        FastAPI: FastAPI endpoint
    """
    app = FastAPI(
        title="Connex API", generate_unique_id_function=lambda route: route.name
    )

    @app.post("/register", tags=["connex"])
    def register_user(user: User):
        try:
            insert.insert_user(user)
            return user.email
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(exc),
            ) from exc

    @app.post("/login", response_model=str, tags=["connex"])
    def login(user: User):
        try:
            secret = select.select_secret(user.email)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(exc),
            ) from exc
        if secret != user.secret or secret is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect login credentials.",
            )
        else:
            return user.email

    @app.post("/add_endpoint", response_model=str, tags=["connex"])
    def add_endpoint(endpoint: Endpoint):
        try:
            insert.insert_endpoint(endpoint)
            return endpoint.name
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
            ) from exc

    @app.post("/endpoints", response_model=List[Endpoint], tags=["connex"])
    def get_endpoints():
        try:
            endpoints = select.select_endpoints()
            return endpoints
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
            ) from exc

    @app.post("/add_project", response_model=str, tags=["connex"])
    def add_project(project: Project):
        try:
            insert.insert_project(project)
            return project.name
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
            ) from exc

    @app.post("/all_projects", response_model=List[Project], tags=["connex"])
    def get_all_projects():
        try:
            projects = select.select_all_projects()
            return projects
        except Exception as exc:
            print(exc)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
            ) from exc

    @app.post("/project", response_model=Project, tags=["connex"])
    def get_project(project_id: str):
        try:
            project = select.select_project(project_id)
            return project
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
            ) from exc

    return app


def serve():
    """Serve the FastAPI application for Connex."""
    app = get_server()
    print("\n\033[1mConnex\033[0m running on http://{}:{}\n".format("localhost", 5000))
    uvicorn.run(app, host="localhost", port=5000, log_level="error")
