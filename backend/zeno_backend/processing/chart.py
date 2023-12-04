"""Functions for extracting chart data from SQL."""
import json
from typing import Any

from zeno_backend.classes.chart import (
    BeeswarmParameters,
    Chart,
    ChartType,
    HeatmapParameters,
    RadarParameters,
    SlicesMetricsOrModels,
    SlicesOrModels,
    TableParameters,
    XCParameters,
)
from zeno_backend.classes.filter import FilterPredicateGroup, Join
from zeno_backend.classes.metric import Metric
from zeno_backend.classes.slice import Slice
from zeno_backend.database.select import metrics, models, slices
from zeno_backend.processing.filtering import table_filter
from zeno_backend.processing.metrics.map import metric_map


async def get_selected_slices(chart_slices: list[int], project: str) -> list[Slice]:
    """Get the slices of the chart from a list of slice ids.

    Args:
        chart_slices (list[int]): slice ids of the chart.
        project (str): project the user is currently working with.

    Returns:
        list[Slice]: list of slices of the chart.
    """
    if -2 in chart_slices:  # -2 signals that all slices should be selected
        return await slices(project)
    selected_slices = await slices(project, chart_slices)
    if -1 in chart_slices:  # -1 signals that the "all instances" slice should be added
        index = chart_slices.index(-1)
        selected_slices.insert(
            index,
            Slice(
                id=-1,
                slice_name="All instances",
                filter_predicates=FilterPredicateGroup(
                    predicates=[], join=Join.OMITTED
                ),
            ),
        )
    return selected_slices


async def get_selected_metrics(chart_metrics: list[int], project: str) -> list[Metric]:
    """Get the metrics of the chart from a list of chart ids.

    Args:
        chart_metrics (list[int]): metric ids of the chart.
        project (str): project the user is currenlty working with.

    Returns:
        list[Metric]: list of metrics of the chart.
    """
    if -2 in chart_metrics:  # -2 signals that all metrics should be selected
        return await metrics(project)
    return list(
        filter(
            lambda metric: metric.id in chart_metrics,
            await metrics(project)
            + [Metric(id=-1, name="count", type="count", columns=[])],
        )
    )


async def get_selected_models(chart_models: list[str], project: str) -> list[str]:
    """Get the models of the chart from a list of models.

    Args:
        chart_models (list[str]): the list of models of the chart.
        project (str): project the user is currently working with.

    Returns:
        list[str]: list of models of the chart.
    """
    if "" in chart_models:  # all models should be selected
        return await models(project)
    return chart_models


async def xyc_data(chart: Chart, project: str) -> str:
    """Generate data for a chart that is based on x, y, and color values.

    Args:
        chart (Chart): the chart for which to generate data.
        project (str): the project the user is currently working with

    Returns:
        str: the chart data in JSON representation.
    """
    elements: list[dict[str, Any]] = []
    if not (isinstance(chart.parameters, XCParameters)):
        return json.dumps({"table": elements})

    all_metrics = await metrics(project)
    selected_metric = next(
        (x for x in all_metrics if x.id == chart.parameters.metric),
        Metric(id=-1, name="count", type="count", columns=[]),
    )
    selected_slices = await get_selected_slices(chart.parameters.slices, project)
    selected_models = await get_selected_models(chart.parameters.models, project)
    for current_slice in selected_slices:
        for model in selected_models:
            filter_sql = await table_filter(
                project, model, current_slice.filter_predicates
            )
            metric = await metric_map(selected_metric, project, model, filter_sql)
            elements.append(
                {
                    "x_value": current_slice.slice_name
                    if chart.parameters.x_channel == SlicesOrModels.SLICES
                    else model,
                    "color_value": model
                    if chart.parameters.color_channel == SlicesOrModels.MODELS
                    else current_slice.slice_name,
                    "y_value": metric.metric,
                    "size": metric.size,
                }
            )

    return json.dumps({"table": elements})


async def table_data(chart: Chart, project: str) -> str:
    """Generate data for a tabular visualization.

    Args:
        chart (Chart): the chart for which to generate data.
        project (str): the project the user is currently working with

    Returns:
        str: the chart data in JSON representation.
    """
    elements: list[dict[str, Any]] = []
    params = chart.parameters
    if not isinstance(params, TableParameters):
        return json.dumps({"table": elements})
    selected_metrics = await get_selected_metrics(params.metrics, project)
    selected_slices = await get_selected_slices(params.slices, project)
    selected_models = await get_selected_models(params.models, project)

    for current_metric in selected_metrics:
        for current_slice in selected_slices:
            for model in selected_models:
                filter_sql = await table_filter(
                    project, model, current_slice.filter_predicates
                )
                metric = await metric_map(current_metric, project, model, filter_sql)
                elements.append(
                    {
                        "x_value": current_slice.id
                        if params.x_channel == SlicesMetricsOrModels.SLICES
                        else model
                        if params.x_channel == SlicesMetricsOrModels.MODELS
                        else current_metric.id,
                        "fixed_value": metric.metric,
                        "y_value": current_slice.id
                        if params.y_channel == SlicesOrModels.SLICES
                        else model,
                        "size": metric.size,
                    }
                )
    return json.dumps({"table": elements})


async def beeswarm_data(chart: Chart, project: str) -> str:
    """Generate data for a beeswarm visualization.

    Args:
        chart (Chart): the chart for which to generate data.
        project (str): the project the user is currently working with

    Returns:
        str: the chart data in JSON representation.
    """
    elements: list[dict[str, Any]] = []
    params = chart.parameters
    if not (isinstance(params, BeeswarmParameters)):
        return json.dumps({"table": elements})
    selected_metrics = await get_selected_metrics(params.metrics, project)
    selected_slices = await get_selected_slices(params.slices, project)
    selected_models = await get_selected_models(params.models, project)

    for current_metric in selected_metrics:
        for current_slice in selected_slices:
            for model in selected_models:
                filter_sql = await table_filter(
                    project, model, current_slice.filter_predicates
                )
                metric = await metric_map(current_metric, project, model, filter_sql)
                elements.append(
                    {
                        "color_value": current_slice.slice_name
                        if params.color_channel == SlicesOrModels.SLICES
                        else model,
                        "x_value": metric.metric,
                        "y_value": current_slice.slice_name
                        if params.y_channel == SlicesOrModels.SLICES
                        else model,
                        "size": metric.size,
                        "metric": current_metric.name,
                    }
                )
    return json.dumps({"table": elements})


async def radar_data(chart: Chart, project: str) -> str:
    """Generate data for a radar chart.

    Args:
        chart (Chart): the chart for which to generate data.
        project (str): the project the user is currently working with

    Returns:
        str: the chart data in JSON representation.
    """
    elements: list[dict[str, Any]] = []
    params = chart.parameters
    if not (isinstance(params, RadarParameters)):
        return json.dumps({"table": elements})
    selected_metrics = await get_selected_metrics(params.metrics, project)
    selected_slices = await get_selected_slices(params.slices, project)
    selected_models = await get_selected_models(params.models, project)

    for current_metric in selected_metrics:
        for current_slice in selected_slices:
            for model in selected_models:
                filter_sql = await table_filter(
                    project, model, current_slice.filter_predicates
                )
                metric = await metric_map(current_metric, project, model, filter_sql)
                elements.append(
                    {
                        "axis_value": current_slice.slice_name
                        if params.axis_channel == SlicesMetricsOrModels.SLICES
                        else model
                        if params.axis_channel == SlicesMetricsOrModels.MODELS
                        else current_metric.name,
                        "fixed_value": metric.metric,
                        "layer_value": current_slice.slice_name
                        if params.layer_channel == SlicesOrModels.SLICES
                        else model,
                        "size": metric.size,
                    }
                )
    return json.dumps({"table": elements})


async def heatmap_data(chart: Chart, project: str) -> str:
    """Generate data for a heatmap visualization.

    Args:
        chart (Chart): the chart for which to generate data.
        project (str): the project the user is currently working with

    Returns:
        str: the chart data in JSON representation.
    """
    elements: list[dict[str, Any]] = []
    params = chart.parameters
    if not (isinstance(params, HeatmapParameters)):
        return json.dumps({"table": elements})
    selected_metric = next(
        (x for x in await metrics(project) if x.id == params.metric),
        Metric(id=-1, name="count", type="count", columns=[]),
    )
    x_slice = params.x_channel == SlicesOrModels.SLICES
    y_slice = params.y_channel == SlicesOrModels.SLICES
    selected_x = (
        await get_selected_slices(params.x_values, project)  # type: ignore
        if x_slice
        else await get_selected_models(params.x_values, project)  # type: ignore
    )
    if x_slice and -1 in params.x_values:
        selected_x = selected_x + [
            Slice(
                id=-1,
                slice_name="All instances",
                filter_predicates=FilterPredicateGroup(
                    predicates=[], join=Join.OMITTED
                ),
            )
        ]

    selected_y = (
        await get_selected_slices(params.y_values, project)  # type: ignore
        if y_slice
        else await get_selected_models(params.y_values, project)  # type: ignore
    )

    for current_x in selected_x:
        for current_y in selected_y:
            metric = {"metric": None, "size": 0}
            if x_slice and y_slice:
                if len(current_x.filter_predicates.predicates) != 0:  # type: ignore
                    current_y.filter_predicates.join = Join.AND  # type: ignore
                if (
                    len(current_y.filter_predicates.predicates) == 0  # type: ignore
                    and len(current_x.filter_predicates.predicates) == 0  # type: ignore
                ):
                    pred_group = None
                else:
                    pred_group = FilterPredicateGroup(
                        predicates=[
                            current_x.filter_predicates,  # type: ignore
                            current_y.filter_predicates,  # type: ignore
                        ],
                        join=Join.OMITTED,
                    )
                filter_sql = await table_filter(project, params.model, pred_group)
                metric = await metric_map(
                    selected_metric, project, params.model, filter_sql
                )
            else:
                filter_sql = await table_filter(
                    project,
                    params.model,
                    (
                        current_x.filter_predicates  # type: ignore
                        if x_slice
                        else current_y.filter_predicates  # type: ignore
                    ),
                )
                metric = await metric_map(
                    selected_metric, project, params.model, filter_sql
                )
            elements.append(
                {
                    "x_value": current_x.slice_name  # type: ignore
                    if x_slice
                    else current_x,
                    "fixed_value": metric.metric,
                    "y_value": current_y.slice_name  # type: ignore
                    if y_slice
                    else current_y,
                    "size": metric.size,
                }
            )
    return json.dumps({"table": elements})


async def calculate_chart_data(chart: Chart, project: str) -> str:
    """Extract the chart data for a specific chart that the user created.

    Args:
        chart (Chart): the chart for which to generate data.
        project (str): the project the user is currently working with

    Returns:
        str: JSON representation of the chart data the user requested.
    """
    if chart.type == ChartType.BAR or chart.type == ChartType.LINE:
        return await xyc_data(chart, project)
    elif chart.type == ChartType.TABLE:
        return await table_data(chart, project)
    elif chart.type == ChartType.BEESWARM:
        return await beeswarm_data(chart, project)
    elif chart.type == ChartType.RADAR:
        return await radar_data(chart, project)
    elif chart.type == ChartType.HEATMAP:
        return await heatmap_data(chart, project)
    else:
        return json.dumps({"table": []})
