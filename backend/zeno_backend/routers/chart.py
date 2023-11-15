"""FastAPI server endpoints for data-table-related queries."""
from amplitude import BaseEvent
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
)

import zeno_backend.database.delete as delete
import zeno_backend.database.insert as insert
import zeno_backend.database.select as select
import zeno_backend.database.update as update
import zeno_backend.util as util
from zeno_backend.classes.amplitude import AmplitudeHandler
from zeno_backend.classes.chart import Chart, ChartResponse
from zeno_backend.processing.chart import chart_data

router = APIRouter(tags=["zeno"])


@router.get(
    "/charts/{owner}/{project}",
    response_model=list[Chart],
    tags=["zeno"],
)
def get_charts(project_uuid: str, request: Request):
    """Get all charts of a project.

    Args:
        project_uuid (str): UUID of the project to get all charts for.
        request (Request): http request to get user information from.

    Returns:
        list[Chart]: list of all of a project's charts.
    """
    util.project_access_valid(project_uuid, request)
    return select.charts(project_uuid)


@router.get(
    "/chart/{owner}/{project}/{chart_id}",
    response_model=ChartResponse,
    tags=["zeno"],
)
def get_chart(project_uuid: str, chart_id: int, request: Request):
    """Get a chart by its id.

    Args:
        project_uuid (str): UUID of the project to get a chart from.
        chart_id (int): id of the chart to be fetched.
        request (Request): http request to get user information from.

    Raises:
        HTTPException: error if the chart could not be fetched.

    Returns:
        ChartResponse: chart spec and data.
    """
    project = select.project_from_uuid(project_uuid)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    util.project_access_valid(project_uuid, request)
    chart = select.chart(project_uuid, chart_id)
    if chart is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chart not found"
        )
    return ChartResponse(chart=chart, chart_data=chart_data(chart, project_uuid))


@router.get(
    "/chart-data/{project_uuid}/{chart_id}",
    response_model=str,
    tags=["zeno"],
)
def get_chart_data(project_uuid: str, chart_id: int, request: Request):
    """Get the data for a chart.

    Args:
        project_uuid (str): UUID of the project to get a chart from.
        chart_id (int): id of the chart to be fetched.
        request (Request): http request to get user information from.

    Raises:
        HTTPException: error if the chart data could not be fetched.

    Returns:
        str: data for the chart in json representation.
    """
    chart = select.chart(project_uuid, chart_id)
    if chart is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chart not found"
        )
    return chart_data(chart, project_uuid)


@router.post(
    "/charts-for-projects/",
    response_model=list[Chart],
    tags=["zeno"],
)
def get_charts_for_projects(project_uuids: list[str]):
    """Get all charts for a list of projects.

    Args:
        project_uuids (list[str]): list of UUIDs of projects to fetch all charts for.

    Returns:
        list[Chart]: all charts for the list of projects
    """
    return select.charts_for_projects(project_uuids)


@router.post(
    "/chart/{project_uuid}",
    response_model=int,
    tags=["zeno"],
)
def add_chart(project_uuid: str, chart: Chart, current_user=Depends(util.auth.claim())):
    """Add a new chart to a project.

    Args:
        project_uuid (str): UUID of the project to add a chart to.
        chart (Chart): chart to be added to the project.
        current_user (Any, optional): user making the addition of the chart.
            Defaults to Depends(util.auth.claim()).

    Raises:
        HTTPException: error if the chart could not be added.

    Returns:
        int: id of the newly added chart.
    """
    id = insert.chart(project_uuid, chart)
    if id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to insert chart",
        )
    AmplitudeHandler().track(
        BaseEvent(
            event_type="Chart Created",
            user_id=current_user["sub"],
            event_properties={"project_uuid": project_uuid},
        )
    )
    return id


@router.patch("/chart/{project_uuid}", tags=["zeno"], dependencies=[Depends(util.auth)])
def update_chart(chart: Chart, project_uuid: str):
    """Update a chart.

    Args:
        chart (Chart): new chart data.
        project_uuid (str): UUID of the project that holds the chart.
    """
    update.chart(chart, project_uuid)


@router.delete("/chart", tags=["zeno"], dependencies=[Depends(util.auth)])
def delete_chart(chart: Chart):
    """Delete a chart from the database.

    Args:
        chart (Chart): chart to be deleted.
    """
    delete.chart(chart)
