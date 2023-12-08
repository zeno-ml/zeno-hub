"""Functions around a project's home elements."""
from fastapi import HTTPException, status

import zeno_backend.database.insert as insert
import zeno_backend.database.select as select
from zeno_backend.classes.chart import (
    Chart,
    ChartType,
    SlicesMetricsOrModels,
    SlicesOrModels,
    TableParameters,
)
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

    table_id = await insert.chart(
        project_uuid,
        Chart(
            id=-1,
            name="Overview Table",
            project_uuid=project_uuid,
            type=ChartType.TABLE,
            parameters=TableParameters(
                metrics=[-1],
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
            width=40,
            height=50,
        ),
    )

    elements = await select.project_home_elements(project_uuid)

    if elements is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not load project home elements.",
        )

    return elements
