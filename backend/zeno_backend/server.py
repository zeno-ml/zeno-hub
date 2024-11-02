"""The FastAPI server for the Zeno backend. Provides endpoints to load data."""

import logging
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware

from zeno_backend.routers import (
    account,
    chart,
    folder,
    metadata,
    metric,
    project,
    report,
    sdk,
    slice,
    table,
    tag,
)


class EndpointFilter(logging.Filter):
    """Filtering endpoints for logging."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter what endpoints are logged for the server.

        Args:
            record (logging.LogRecord): the log record for the application.

        Returns:
            bool: whether or not to log the endpoint.
        """
        return record.getMessage().find("/ping") == -1


def get_server() -> FastAPI:
    """Provide the FastAPI server and specifies its inputs.

    Returns:
        FastAPI: FastAPI endpoint
    """
    app = FastAPI(title="Frontend API", separate_input_output_schemas=False)
    # Filter out /endpoint
    logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

    # load env vars for cognito if available
    env_path = Path("../frontend/.env")
    if env_path.exists():
        load_dotenv(env_path)

    # if we have a CORS_ORIGIN variable in the environment, add middleware
    if "CORS_ORIGIN" in os.environ:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[os.environ["CORS_ORIGIN"]],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    api_app = FastAPI(
        title="Backend API",
        generate_unique_id_function=lambda route: route.name,
        separate_input_output_schemas=False,
    )
    api_app.include_router(account.router)
    api_app.include_router(chart.router)
    api_app.include_router(folder.router)
    api_app.include_router(metadata.router)
    api_app.include_router(metric.router)
    api_app.include_router(project.router)
    api_app.include_router(report.router)
    api_app.include_router(sdk.router)
    api_app.include_router(slice.router)
    api_app.include_router(table.router)
    api_app.include_router(tag.router)

    @api_app.middleware("http")
    async def log_process_time(request: Request, call_next):
        start_time = time.time()
        logging.info(f"{request.method}\t {request.url.path}")
        response = await call_next(request)
        process_time = time.time() - start_time
        logging.info(
            f"{request.method}\t {request.url.path} "
            f"{response.status_code} {process_time:.2f}ms"
        )
        return response

    app.mount("/api", api_app)

    # ping server route to check if live
    @app.get("/ping")
    def ping():
        return Response(status_code=status.HTTP_200_OK)

    return app
