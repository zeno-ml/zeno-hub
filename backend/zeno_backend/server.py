"""The FastAPI server for the Zeno backend. Provides endpoints to load data."""

from pathlib import Path
from typing import List, Union

import pandas as pd
import uvicorn
from fastapi import FastAPI, File, HTTPException, Response, UploadFile, status

import zeno_backend.database.delete as delete
import zeno_backend.database.insert as insert
import zeno_backend.database.select as select
import zeno_backend.database.update as update
from zeno_backend.classes.base import (
    GroupMetric,
    LabelSpec,
    OutputSpec,
    PostdistillSpec,
    PredistillSpec,
    ProjectConfig,
    ZenoColumn,
)
from zeno_backend.classes.chart import Chart
from zeno_backend.classes.folder import Folder
from zeno_backend.classes.metadata import HistogramBucket
from zeno_backend.classes.metric import Metric, MetricRequest
from zeno_backend.classes.slice import Slice
from zeno_backend.classes.slice_finder import SliceFinderRequest, SliceFinderReturn
from zeno_backend.classes.table import TableRequest
from zeno_backend.classes.tag import Tag, TagMetricKey
from zeno_backend.processing.chart import chart_data
from zeno_backend.processing.filtering import table_filter
from zeno_backend.processing.histogram_processing import (
    HistogramRequest,
    histogram_buckets,
    histogram_counts,
    histogram_metrics,
)
from zeno_backend.processing.metrics import metric_map
from zeno_backend.processing.slice_finder import slice_finder
from zeno_backend.processing.util import generate_diff_cols, save_file


def get_server() -> FastAPI:
    """Provide the FastAPI server and specifies its inputs.

    Raises:
    ------
        HTTPException: Something goes wrong server-side.

    Returns:
    -------
        FastAPI: FastAPI endpoint
    """
    app = FastAPI(title="Frontend API")
    api_app = FastAPI(
        title="Backend API", generate_unique_id_function=lambda route: route.name
    )
    app.mount("/api", api_app)

    ###################################################################### Fetch
    @api_app.get("/view/{project}", response_model=ProjectConfig, tags=["zeno"])
    def get_project(project: str):
        return select.project(project)

    @api_app.get("/data/{project}", response_model=bytes, tags=["zeno"])
    def get_data(project: str, item: str):
        file_path = Path("data", project, item)
        if not Path.is_file(file_path):
            return Response(status_code=404)
        blob = open(file_path, "rb").read()
        return Response(blob)

    @api_app.get("/models/{project}", response_model=List[str], tags=["zeno"])
    def get_models(project: str):
        return select.models(project)

    @api_app.get("/metrics/{project}", response_model=List[Metric], tags=["zeno"])
    def get_metrics(project: str):
        return select.metrics(project)

    @api_app.get("/folders/{project}", response_model=List[Folder], tags=["zeno"])
    def get_folders(project: str):
        return select.folders(project)

    @api_app.get("/slices/{project}", response_model=List[Slice], tags=["zeno"])
    def get_slices(project: str):
        return select.slices(project)

    @api_app.get("/charts/{project}", response_model=List[Chart], tags=["zeno"])
    def get_charts(project: str):
        return select.charts(project)

    @api_app.get("/columns/{project}", response_model=List[ZenoColumn], tags=["zeno"])
    def get_columns(project: str):
        return select.columns(project)

    @api_app.get("/tags/{project}", response_model=List[Tag], tags=["zeno"])
    def get_tags(project: str):
        return select.tags(project)

    ####################################################################### Post
    @api_app.post("/project", tags=["zeno"])
    def add_project(description: ProjectConfig):
        try:
            Path("data", description.uuid).mkdir()
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=("ERROR: Project already exists."),
            ) from exc
        insert.setup_project(description)
        return description.uuid

    @api_app.post("/item/{project}", tags=["zeno"])
    async def add_item(project: str, name: str, file: UploadFile = File(...)):
        insert.item(name, project)
        file_path = Path("data", project, name)
        parent_path = file_path.parent
        if not parent_path.exists():
            parent_path.mkdir(parents=True)
        return await save_file(file_path, file)

    @api_app.post("/label/{project}", tags=["zeno"])
    def add_label(project: str, label_spec: LabelSpec):
        insert.label(label_spec, project)
        return label_spec.label

    @api_app.post("/output/{project}", tags=["zeno"])
    def add_output(project: str, output_spec: OutputSpec):
        insert.output(output_spec, project)
        return output_spec.model

    @api_app.post("/predistill/{project}", tags=["zeno"])
    def add_predistill(project: str, predistill_spec: PredistillSpec):
        insert.predistill(predistill_spec, project)
        return predistill_spec.value

    @api_app.post("/postdistill/{project}", tags=["zeno"])
    def add_postdistill(project: str, postdistill_spec: PostdistillSpec):
        insert.postdistill(postdistill_spec, project)
        return postdistill_spec.value

    @api_app.post("/folder/{project}", tags=["zeno"])
    def add_folder(project: str, name: str):
        insert.folder(project, name)
        return name

    @api_app.post("/slice/{project}", tags=["zeno"])
    def add_slice(project: str, req: Slice):
        insert.slice(project, req)
        return req.slice_name

    @api_app.post("/chart/{project}", tags=["zeno"])
    def add_chart(project: str, chart: Chart):
        insert.chart(project, chart)
        return chart.name

    @api_app.post(
        "/slice-metrics/{project}", response_model=List[GroupMetric], tags=["zeno"]
    )
    def get_metrics_for_slices(req: MetricRequest, project: str):
        return_metrics: List[GroupMetric] = []
        for metric_key in req.metric_keys:
            filter_sql = table_filter(
                project, metric_key.model, metric_key.slice.filter_predicates, req.items
            )
            return_metrics.append(
                metric_map(metric_key.metric, project, metric_key.model, filter_sql)
            )
        return return_metrics

    @api_app.post(
        "/histograms/{project}",
        response_model=List[List[HistogramBucket]],
        tags=["zeno"],
    )
    def get_histogram_buckets(req: List[ZenoColumn], project: str):
        return histogram_buckets(project, req)

    @api_app.post(
        "/histogram-counts/{project}", response_model=List[List[int]], tags=["zeno"]
    )
    def calculate_histogram_counts(req: HistogramRequest, project: str):
        return histogram_counts(project, req)

    @api_app.post(
        "/histogram-metrics/{project}",
        response_model=List[List[Union[float, None]]],
        tags=["zeno"],
    )
    def calculate_histogram_metrics(req: HistogramRequest, project: str):
        return histogram_metrics(project, req)

    @api_app.post("/tag/{project}", tags=["zeno"])
    def add_tag(tag: Tag, project: str):
        insert.tag(project, tag)
        return tag.tag_name

    @api_app.post("/tag-metric/{project}", response_model=GroupMetric, tags=["zeno"])
    def get_metric_for_tag(metric_key: TagMetricKey, project: str):
        filter_sql = table_filter(project, metric_key.model, None, metric_key.tag.items)
        return metric_map(metric_key.metric, project, metric_key.model, filter_sql)

    @api_app.post(
        "/slice-finder/{project}", tags=["zeno"], response_model=SliceFinderReturn
    )
    def run_slice_finder(req: SliceFinderRequest, project: str):
        return slice_finder(project, req)

    @api_app.post("/filtered-table/{project}", response_model=str, tags=["zeno"])
    def get_filtered_table(req: TableRequest, project: str):
        filter_sql = table_filter(project, None, req.filter_predicates, req.items)
        sql_table = select.table_data_paginated(
            project, filter_sql, req.offset, req.limit
        )
        filt_df = pd.DataFrame(sql_table.table, columns=sql_table.columns)
        if req.diff_column_1 and req.diff_column_2:
            filt_df = generate_diff_cols(
                filt_df, req.diff_column_1, req.diff_column_2, project
            )
        return filt_df.to_json(orient="records")

    @api_app.post("/chart-data/{project}", tags=["zeno"], response_model=str)
    def get_chart_data(chart: Chart, project: str):
        return chart_data(chart, project)

    ####################################################################### Update
    @api_app.post("/slice/update/{project}", tags=["zeno"])
    def update_slice(req: Slice, project: str):
        update.slice(req, project)
        return req.slice_name

    @api_app.post("/chart/update/{project}", tags=["zeno"])
    def update_chart(chart: Chart, project: str):
        update.chart(chart, project)
        return chart.name

    @api_app.post("/folder/update/{project}", tags=["zeno"])
    def update_folder(folder: Folder, project: str):
        update.folder(folder, project)
        return folder.name

    @api_app.post("/tag/update/{project}", tags=["zeno"])
    def update_tag(tag: Tag, project: str):
        update.tag(tag, project)
        return tag.tag_name

    ####################################################################### Delete
    @api_app.delete("/slice", tags=["zeno"])
    def delete_slice(req: Slice):
        delete.slice(req)
        return req.slice_name

    @api_app.delete("/chart", tags=["zeno"])
    def delete_chart(chart: Chart):
        delete.chart(chart)
        return chart.name

    @api_app.delete("/folder", tags=["zeno"])
    def delete_folder(folder: Folder):
        delete.folder(folder)
        return folder.name

    @api_app.delete("/tag", tags=["zeno"])
    def delete_tag(tag: Tag):
        delete.tag(tag)
        return tag.tag_name

    return app


def serve():
    """Serve the FastAPI application for the backend."""
    app = get_server()
    print(
        "\n\033[1mZeno server\033[0m running on http://{}:{}\n".format(
            "localhost", 8000
        )
    )
    uvicorn.run(app, host="localhost", port=8000, log_level="error")
