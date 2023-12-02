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
from zeno_backend.classes.chart import Chart
from zeno_backend.processing.chart import calculate_chart_data

router = APIRouter(tags=["zeno"])


@router.get(
    "/charts/{owner}/{project}",
    response_model=list[Chart],
    tags=["zeno"],
)
async def get_charts(project_uuid: str, request: Request):
    """Get all charts of a project.

    Args:
        project_uuid (str): UUID of the project to get all charts for.
        request (Request): http request to get user information from.

    Returns:
        list[Chart]: list of all of a project's charts.
    """
    await util.project_access_valid(project_uuid, request)
    return await select.charts(project_uuid)


@router.get(
    "/chart/{owner}/{project}/{chart_id}",
    response_model=Chart,
    tags=["zeno"],
)
async def get_chart(project_uuid: str, chart_id: int, request: Request):
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
    await util.project_access_valid(project_uuid, request)
    chart = await select.chart(project_uuid, chart_id)
    if chart.data is None:
        chart_output = await calculate_chart_data(chart, project_uuid)
        await update.chart_data(chart_id, chart_output)
        chart.data = chart_output

    return chart


@router.post(
    "/charts-for-projects/",
    response_model=list[Chart],
    tags=["zeno"],
)
async def get_charts_for_projects(project_uuids: list[str], request: Request):
    """Get all charts for a list of projects.

    Args:
        project_uuids (list[str]): list of UUIDs of projects to fetch all charts for.
        request (Request): http request to get user information from.

    Returns:
        list[Chart]: all charts for the list of projects
    """
    if len(project_uuids) == 0:
        return []

    for project_uuid in project_uuids:
        await util.project_access_valid(project_uuid, request)
    charts = await select.charts_for_projects(project_uuids)
    for c in charts:
        if c.data is None:
            chart_output = await calculate_chart_data(c, c.project_uuid)
            await update.chart_data(c.id, chart_output)
            c.data = chart_output
    return charts


@router.post(
    "/chart/{project_uuid}",
    response_model=int,
    tags=["zeno"],
)
async def add_chart(
    project_uuid: str,
    chart: Chart,
    request: Request,
    current_user=Depends(util.auth.claim()),
):
    """Add a new chart to a project.

    Args:
        project_uuid (str): UUID of the project to add a chart to.
        chart (Chart): chart to be added to the project.
        request (Request): http request to get user information from.
        current_user (Any, optional): user making the addition of the chart.
            Defaults to Depends(util.auth.claim()).

    Raises:
        HTTPException: error if the chart could not be added.

    Returns:
        int: id of the newly added chart.
    """
    await util.project_editor(project_uuid, request)
    id = await insert.chart(project_uuid, chart)
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


@router.patch(
    "/chart/{project_uuid}",
    response_model=str,
    tags=["zeno"],
    dependencies=[Depends(util.auth)],
)
async def update_chart(chart: Chart, project_uuid: str, request: Request):
    """Update a chart.

    Args:
        chart (Chart): new chart data.
        project_uuid (str): UUID of the project that holds the chart.
        request (Request): http request to get user information from.
    """
    await util.project_editor(project_uuid, request)
    return await update.chart(chart, project_uuid)


@router.delete(
    "/chart/{project_uuid}/{chart_id}", tags=["zeno"], dependencies=[Depends(util.auth)]
)
async def delete_chart(project_uuid: str, chart_id: int, request: Request):
    """Delete a chart from the database.

    Args:
        project_uuid (str): project to which the chart belongs.
        chart_id (int): id of the chart to be deleted.
        request (Request): http request to get user information from.
    """
    await util.project_editor(project_uuid, request)
    await delete.chart(chart_id)
