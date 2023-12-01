"""FastAPI server endpoints for metric-related queries."""

from fastapi import (
    APIRouter,
    Request,
)

import zeno_backend.database.select as select
import zeno_backend.util as util
from zeno_backend.classes.base import (
    GroupMetric,
)
from zeno_backend.classes.metric import Metric, MetricRequest
from zeno_backend.classes.tag import TagMetricKey
from zeno_backend.processing.filtering import table_filter
from zeno_backend.processing.metrics.map import metric_map

router = APIRouter(tags=["zeno"])


@router.get(
    "/metrics/{project_uuid}",
    response_model=list[Metric],
    tags=["zeno"],
)
async def get_metrics(project_uuid: str, request: Request):
    """Get all metrics for a specific project.

    Args:
        project_uuid (str): UUID of the project to fetch metrics for.
        request (Request): http request to get user information from.

    Returns:
        list[Metric]: all metrics associated with a specific project.
    """
    await util.project_access_valid(project_uuid, request)
    return await select.metrics(project_uuid)


@router.post(
    "/slice-metrics/{project_uuid}",
    response_model=list[GroupMetric],
    tags=["zeno"],
)
async def get_metrics_filtered(req: MetricRequest, project_uuid: str, request: Request):
    """Get all metrics that match a metrics query.

    Args:
        req (MetricRequest): request specification for the metrics to be fetched.
        project_uuid (str): UUID of the project to fetch metrics for.
        request (Request): http request to get user information from.

    Returns:
        list[Metric]: metrics that match the metric request.
    """
    await util.project_access_valid(project_uuid, request)
    return_metrics: list[GroupMetric] = []
    metrics = await select.metrics_by_id(
        [m.metric for m in req.metric_keys], project_uuid
    )
    for metric_key in req.metric_keys:
        filter_sql = await table_filter(
            project_uuid,
            metric_key.model,
            metric_key.slice.filter_predicates,
            req.data_ids,
        )
        return_metrics.append(
            await metric_map(
                metrics.get(metric_key.metric),
                project_uuid,
                metric_key.model,
                filter_sql,
            )
        )
    return return_metrics


@router.post(
    "/tag-metric/{project_uuid}",
    response_model=GroupMetric,
    tags=["zeno"],
)
async def get_metric_for_tag(
    metric_key: TagMetricKey, project_uuid: str, request: Request
):
    """Get the metric for a specific tag.

    Args:
        metric_key (TagMetricKey): specification for which tag to calculate the metric.
        project_uuid (str): UUID of the project to calculate the metric for.
        request (Request): http request to get user information from.

    Returns:
        GroupMetric: the metric calculation result.
    """
    await util.project_access_valid(project_uuid, request)
    filter_sql = await table_filter(
        project_uuid, metric_key.model, None, metric_key.tag.data_ids
    )

    if metric_key.metric is None:
        return await metric_map(None, project_uuid, metric_key.model, filter_sql)

    metric = await select.metrics_by_id([metric_key.metric], project_uuid)
    return await metric_map(
        metric.get(metric_key.metric), project_uuid, metric_key.model, filter_sql
    )
