"""Functions around a project's home elements."""
import math

from fastapi import HTTPException, status

import zeno_backend.database.insert as insert
import zeno_backend.database.select as select
from zeno_backend.classes.chart import (
    Chart,
    ChartType,
    RadarParameters,
    SlicesMetricsOrModels,
    SlicesOrModels,
    TableParameters,
    XCParameters,
)
from zeno_backend.classes.metric import Metric
from zeno_backend.classes.project import ProjectHomeElement, ProjectHomeElementType


async def create_project_home(project_uuid) -> list[ProjectHomeElement]:
    """Create the data for a project's home page.

    Args:
        project_uuid (str): the uuid of the project for which to create home elements.

    Returns:
        list[ProjectHomeElement]: list of home elements of the project.
    """
    metrics = await select.metrics(project_uuid)
    models = await select.models(project_uuid)

    if len(metrics) == 0 or len(models) == 0:
        return []

    await create_overview_table(project_uuid)
    await create_overview_charts(project_uuid, metrics)
    await insert.project_home_element(
        project_uuid,
        ProjectHomeElement(
            id=-1,
            type=ProjectHomeElementType.LIST,
            x_pos=30,
            y_pos=0,
            width=70,
            height=100,
        ),
    )

    elements = await select.project_home_elements(project_uuid)

    if elements is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not load project home elements.",
        )

    return elements


async def create_overview_table(project_uuid: str):
    """Create an overview table of all models for all metrics.

    Args:
        project_uuid (str): the uuid of the project to create the table for.
    """
    table_id = await insert.chart(
        project_uuid,
        Chart(
            id=-1,
            name="Model Performance (Table)",
            project_uuid=project_uuid,
            type=ChartType.TABLE,
            parameters=TableParameters(
                metrics=[-2],
                slices=[-1],
                models=[""],
                y_channel=SlicesOrModels.MODELS,
                x_channel=SlicesMetricsOrModels.METRICS,
                fixed_channel=SlicesMetricsOrModels.SLICES,
            ),
        ),
    )

    if table_id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not add overview table to the project.",
        )

    await insert.project_home_element(
        project_uuid,
        ProjectHomeElement(
            id=-1,
            type=ProjectHomeElementType.CHART,
            data=str(table_id),
            x_pos=0,
            y_pos=0,
            width=30,
            height=50,
        ),
    )


async def create_overview_charts(project_uuid: str, metrics: list[Metric]):
    """Create an overview chart of all models for all metrics.

    Args:
        project_uuid (str): the uuid of the project to create the chart for.
        metrics (list[Metric]): the metrics that can be used in the chart.
    """
    if len(metrics) > 2:
        chart_id = await insert.chart(
            project_uuid,
            Chart(
                id=-1,
                name="Model Performance (Radar)",
                project_uuid=project_uuid,
                type=ChartType.RADAR,
                parameters=RadarParameters(
                    metrics=[-2],
                    slices=[-1],
                    models=[""],
                    axis_channel=SlicesMetricsOrModels.METRICS,
                    layer_channel=SlicesOrModels.MODELS,
                    fixed_channel=SlicesMetricsOrModels.SLICES,
                ),
            ),
        )

        if chart_id is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not add overview table to the project.",
            )

        await insert.project_home_element(
            project_uuid,
            ProjectHomeElement(
                id=-1,
                type=ProjectHomeElementType.CHART,
                data=str(chart_id),
                x_pos=0,
                y_pos=50,
                width=30,
                height=50,
            ),
        )
    else:
        for metric_index, metric in enumerate(metrics):
            chart_id = await insert.chart(
                project_uuid,
                Chart(
                    id=-1,
                    name=metric.name,
                    project_uuid=project_uuid,
                    type=ChartType.BAR,
                    parameters=XCParameters(
                        slices=[-1],
                        metric=metric.id,
                        models=[""],
                        color_channel=SlicesOrModels.MODELS,
                        x_channel=SlicesOrModels.SLICES,
                    ),
                ),
            )

            if chart_id is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Could not add overview table to the project.",
                )

            await insert.project_home_element(
                project_uuid,
                ProjectHomeElement(
                    id=-1,
                    type=ProjectHomeElementType.CHART,
                    data=str(chart_id),
                    x_pos=0,
                    y_pos=50 + (metric_index * math.ceil(50 / len(metrics))),
                    width=30,
                    height=math.floor(50 / len(metrics)),
                ),
            )
