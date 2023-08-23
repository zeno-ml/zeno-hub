"""The FastAPI server for the Zeno backend. Provides endpoints to load data."""
import os
import shutil
import uuid
from pathlib import Path

import pandas as pd
import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, HTTPException, Response, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cloudauth.cognito import Cognito

import zeno_backend.database.delete as delete
import zeno_backend.database.insert as insert
import zeno_backend.database.select as select
import zeno_backend.database.update as update
from zeno_backend.classes.base import (
    DataSpec,
    FeatureSpec,
    GroupMetric,
    LabelSpec,
    OutputSpec,
    ZenoColumn,
)
from zeno_backend.classes.chart import Chart
from zeno_backend.classes.folder import Folder
from zeno_backend.classes.metadata import HistogramBucket, StringFilterRequest
from zeno_backend.classes.metric import Metric, MetricRequest
from zeno_backend.classes.project import Project, ProjectStats
from zeno_backend.classes.slice import Slice
from zeno_backend.classes.slice_finder import SliceFinderRequest, SliceFinderReturn
from zeno_backend.classes.table import TableRequest
from zeno_backend.classes.tag import Tag, TagMetricKey
from zeno_backend.classes.user import Organization, User
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

    # load env vars for cognito if available
    env_path = Path("../frontend/.env")
    if env_path.exists():
        load_dotenv(env_path)

    # function to get the user from cognito
    auth = Cognito(
        region=os.environ["ZENO_USER_POOL_AUTH_REGION"],
        userPoolId=os.environ["ZENO_USER_POOL_ID"],
        client_id=os.environ["ZENO_USER_POOL_CLIENT_ID"],
    )

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
        title="Backend API", generate_unique_id_function=lambda route: route.name
    )
    app.mount("/api", api_app)

    # ping server route to check if live
    @app.get("/ping")
    def ping():
        return Response(status_code=status.HTTP_200_OK)

    ###################################################################### Fetch
    @api_app.get(
        "/users", response_model=list[User], tags=["zeno"], dependencies=[Depends(auth)]
    )
    def get_users():
        return select.users()

    @api_app.get(
        "/organization_names",
        response_model=list[Organization],
        tags=["zeno"],
        dependencies=[Depends(auth)],
    )
    def get_organization_names():
        return select.organization_names()

    @api_app.get(
        "/data/{project}",
        response_model=bytes,
        tags=["zeno"],
        dependencies=[Depends(auth)],
    )
    def get_data(project: str, data_id: str):
        file_path = Path("data", project, data_id)
        if not Path.is_file(file_path):
            return Response(status_code=404)
        blob = open(file_path, "rb").read()
        return Response(blob)

    @api_app.get(
        "/project_stats/{project}",
        response_model=ProjectStats,
        tags=["zeno"],
        dependencies=[Depends(auth)],
    )
    def get_project_stats(project: str):
        return select.project_stats(project)

    @api_app.get(
        "/models/{project}",
        response_model=list[str],
        tags=["zeno"],
        dependencies=[Depends(auth)],
    )
    def get_models(project: str):
        return select.models(project)

    @api_app.get(
        "/metrics/{project}",
        response_model=list[Metric],
        tags=["zeno"],
        dependencies=[Depends(auth)],
    )
    def get_metrics(project: str):
        return select.metrics(project)

    @api_app.get(
        "/folders/{project}",
        response_model=list[Folder],
        tags=["zeno"],
        dependencies=[Depends(auth)],
    )
    def get_folders(project: str):
        return select.folders(project)

    @api_app.get(
        "/slices/{project}",
        response_model=list[Slice],
        tags=["zeno"],
        dependencies=[Depends(auth)],
    )
    def get_slices(project: str):
        return select.slices(project)

    @api_app.get(
        "/charts/{project}",
        response_model=list[Chart],
        tags=["zeno"],
        dependencies=[Depends(auth)],
    )
    def get_charts(project: str):
        return select.charts(project)

    @api_app.get(
        "/columns/{project}",
        response_model=list[ZenoColumn],
        tags=["zeno"],
        dependencies=[Depends(auth)],
    )
    def get_columns(project: str):
        return select.columns(project)

    @api_app.get(
        "/tags/{project}",
        response_model=list[Tag],
        tags=["zeno"],
        dependencies=[Depends(auth)],
    )
    def get_tags(project: str):
        return select.tags(project)

    @api_app.post(
        "/tag-metric/{project}",
        response_model=GroupMetric,
        tags=["zeno"],
        dependencies=[Depends(auth)],
    )
    def get_metric_for_tag(metric_key: TagMetricKey, project: str):
        filter_sql = table_filter(
            project, metric_key.model, None, metric_key.tag.data_ids
        )
        return metric_map(metric_key.metric, project, metric_key.model, filter_sql)

    @api_app.post(
        "/slice-finder/{project}",
        tags=["zeno"],
        response_model=SliceFinderReturn,
        dependencies=[Depends(auth)],
    )
    def run_slice_finder(req: SliceFinderRequest, project: str):
        return slice_finder(project, req)

    @api_app.post(
        "/filtered-table/{project}",
        response_model=str,
        tags=["zeno"],
        dependencies=[Depends(auth)],
    )
    def get_filtered_table(req: TableRequest, project: str):
        filter_sql = table_filter(project, None, req.filter_predicates, req.data_ids)
        sql_table = select.table_data_paginated(
            project, filter_sql, req.offset, req.limit
        )
        filt_df = pd.DataFrame(sql_table.table, columns=sql_table.columns)
        if req.diff_column_1 and req.diff_column_2:
            filt_df = generate_diff_cols(
                filt_df, req.diff_column_1, req.diff_column_2, project
            )
        return filt_df.to_json(orient="records")

    @api_app.post(
        "/chart-data/{project}",
        tags=["zeno"],
        response_model=str,
        dependencies=[Depends(auth)],
    )
    def get_chart_data(chart: Chart, project: str):
        return chart_data(chart, project)

    @api_app.post("/organizations", tags=["zeno"], response_model=list[Organization])
    def get_organizations(current_user=Depends(auth.claim())):
        user = select.user(current_user["username"])
        if user is None:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return select.organizations(user)

    @api_app.post("/project/{owner}/{project}", response_model=Project, tags=["zeno"])
    def get_project(
        owner_name: str, project_name: str, current_user=Depends(auth.claim())
    ):
        user = select.user(current_user["username"])
        if user is None:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return select.project(owner_name, project_name, user)

    @api_app.get(
        "/project-uuid/{owner_name}/{project_name}",
        dependencies=[Depends(auth)],
        tags=["zeno"],
    )
    def get_project_uuid(owner_name: str, project_name: str):
        return select.project_uuid(owner_name, project_name)

    @api_app.get(
        "/projects",
        response_model=list[Project],
        tags=["zeno"],
    )
    def get_projects(current_user=Depends(auth.claim())):
        user = select.user(current_user["username"])
        if user is None:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return select.projects(user)

    @api_app.get(
        "/public_projects",
        response_model=list[Project],
        tags=["zeno"],
    )
    def get_public_projects():
        return select.public_projects()

    @api_app.post(
        "/slice-metrics/{project}",
        response_model=list[GroupMetric],
        tags=["zeno"],
        dependencies=[Depends(auth)],
    )
    def get_metrics_for_slices(req: MetricRequest, project: str):
        return_metrics: list[GroupMetric] = []
        for metric_key in req.metric_keys:
            filter_sql = table_filter(
                project,
                metric_key.model,
                metric_key.slice.filter_predicates,
                req.data_ids,
            )
            return_metrics.append(
                metric_map(metric_key.metric, project, metric_key.model, filter_sql)
            )
        return return_metrics

    @api_app.post(
        "/histograms/{project}",
        response_model=list[list[HistogramBucket]],
        tags=["zeno"],
        dependencies=[Depends(auth)],
    )
    def get_histogram_buckets(req: list[ZenoColumn], project: str):
        return histogram_buckets(project, req)

    @api_app.post(
        "/histogram-counts/{project}",
        response_model=list[list[int]],
        tags=["zeno"],
        dependencies=[Depends(auth)],
    )
    def calculate_histogram_counts(req: HistogramRequest, project: str):
        return histogram_counts(project, req)

    @api_app.post(
        "/histogram-metrics/{project}",
        response_model=list[list[float | None]],
        tags=["zeno"],
        dependencies=[Depends(auth)],
    )
    def calculate_histogram_metrics(req: HistogramRequest, project: str):
        return histogram_metrics(project, req)

    @api_app.get(
        "/project_users/{project}",
        response_model=list[User],
        tags=["zeno"],
        dependencies=[Depends(auth)],
    )
    def get_project_users(project: str):
        return select.project_users(project)

    @api_app.get(
        "/project_organizations/{project}",
        response_model=list[Organization],
        tags=["zeno"],
        dependencies=[Depends(auth)],
    )
    def get_project_orgs(project: str):
        return select.project_orgs(project)

    @api_app.post(
        "/string-filter/{project}",
        response_model=list[str],
        tags=["zeno"],
        dependencies=[Depends(auth)],
    )
    def filter_string_metadata(project: str, req: StringFilterRequest):
        return select.filered_short_string_column_values(project, req)

    ####################################################################### Insert
    @api_app.post(
        "/login", response_model=User, tags=["zeno"], dependencies=[Depends(auth)]
    )
    def login(name: str):
        try:
            fetched_user = select.user(name)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(exc),
            ) from exc
        if fetched_user is None:
            try:
                insert.user(User(id=-1, name=name, admin=None))
                return select.user(name)
            except Exception as exc:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=str(exc),
                ) from exc
        else:
            return fetched_user

    @api_app.post("/project-create", tags=["zeno"])
    def add_project(project: Project, current_user=Depends(auth.claim())):
        project.uuid = str(uuid.uuid4())
        user = select.user(current_user["username"])
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=("ERROR: User could not be found."),
            )
        insert.project(project, user)
        return project.uuid

    @api_app.post(
        "/upload_datapoint/{project}", tags=["zeno"], dependencies=[Depends(auth)]
    )
    async def upload_datapoint(
        project: str, data_spec: DataSpec, file: UploadFile = File(...)
    ):
        insert.datapoint(data_spec, project)
        file_path = Path("data", project, str(data_spec.data_id))
        parent_path = file_path.parent
        if not parent_path.exists():
            parent_path.mkdir(parents=True)
        await save_file(file_path, file)

    @api_app.post(
        "/add_datapoint/{project}", tags=["zeno"], dependencies=[Depends(auth)]
    )
    def add_datapoint(project: str, data_spec: DataSpec):
        insert.datapoint(data_spec, project)

    @api_app.post("/label/{project}", tags=["zeno"], dependencies=[Depends(auth)])
    def add_label(project: str, label_spec: LabelSpec):
        insert.label(label_spec, project)

    @api_app.post("/output/{project}", tags=["zeno"], dependencies=[Depends(auth)])
    def add_output(project: str, output_spec: OutputSpec):
        insert.output(output_spec, project)

    @api_app.post("/feature/{project}", tags=["zeno"], dependencies=[Depends(auth)])
    def add_feature(project: str, feature_spec: FeatureSpec):
        insert.feature(feature_spec, project)

    @api_app.post("/folder/{project}", tags=["zeno"], dependencies=[Depends(auth)])
    def add_folder(project: str, name: str):
        insert.folder(project, name)

    @api_app.post("/slice/{project}", tags=["zeno"], dependencies=[Depends(auth)])
    def add_slice(project: str, req: Slice):
        insert.slice(project, req)

    @api_app.post("/chart/{project}", tags=["zeno"], dependencies=[Depends(auth)])
    def add_chart(project: str, chart: Chart):
        insert.chart(project, chart)

    @api_app.post("/tag/{project}", tags=["zeno"], dependencies=[Depends(auth)])
    def add_tag(tag: Tag, project: str):
        insert.tag(project, tag)

    @api_app.post("/add_organization", tags=["zeno"], dependencies=[Depends(auth)])
    def add_organization(user: User, organization: Organization):
        insert.organization(user, organization)

    @api_app.post(
        "/add_project_user/{project}", tags=["zeno"], dependencies=[Depends(auth)]
    )
    def add_project_user(project: str, user: User):
        project_obj = select.project_from_uuid(project)
        if project_obj is not None and project_obj.owner_name != user.name:
            insert.project_user(project, user)

    @api_app.post(
        "/add_project_org/{project}", tags=["zeno"], dependencies=[Depends(auth)]
    )
    def add_project_org(project: str, organization: Organization):
        insert.project_org(project, organization)

    ####################################################################### Update
    @api_app.post(
        "/slice/update/{project}", tags=["zeno"], dependencies=[Depends(auth)]
    )
    def update_slice(req: Slice, project: str):
        update.slice(req, project)

    @api_app.post(
        "/chart/update/{project}", tags=["zeno"], dependencies=[Depends(auth)]
    )
    def update_chart(chart: Chart, project: str):
        update.chart(chart, project)

    @api_app.post(
        "/folder/update/{project}", tags=["zeno"], dependencies=[Depends(auth)]
    )
    def update_folder(folder: Folder, project: str):
        update.folder(folder, project)

    @api_app.post("/tag/update/{project}", tags=["zeno"], dependencies=[Depends(auth)])
    def update_tag(tag: Tag, project: str):
        update.tag(tag, project)

    @api_app.post("/user/update", tags=["zeno"], dependencies=[Depends(auth)])
    def update_user(user: User):
        update.user(user)

    @api_app.post("/organization/update", tags=["zeno"], dependencies=[Depends(auth)])
    def update_organization(organization: Organization):
        update.organization(organization)

    @api_app.post("/project/update", tags=["zeno"], dependencies=[Depends(auth)])
    def update_project(project: Project):
        update.project(project)

    @api_app.post(
        "/project_user/update/{project}", tags=["zeno"], dependencies=[Depends(auth)]
    )
    def update_project_user(project: str, user: User):
        update.project_user(project, user)

    @api_app.post(
        "/project_org/update/{project}", tags=["zeno"], dependencies=[Depends(auth)]
    )
    def update_project_org(project: str, organization: Organization):
        update.project_org(project, organization)

    ####################################################################### Delete
    @api_app.delete("/project/{project}", tags=["zeno"])
    def delete_project(project: str, current_user=Depends(auth.claim())):
        project_obj = select.project_from_uuid(project)
        if project_obj is None or project_obj.owner_name != current_user["username"]:
            return  # make sure only project owners can delete a project
        data_path = Path("data", project)
        if data_path.exists():
            shutil.rmtree(data_path)
        delete.project(project)

    @api_app.delete("/slice", tags=["zeno"], dependencies=[Depends(auth)])
    def delete_slice(req: Slice):
        delete.slice(req)

    @api_app.delete("/chart", tags=["zeno"], dependencies=[Depends(auth)])
    def delete_chart(chart: Chart):
        delete.chart(chart)

    @api_app.delete("/folder", tags=["zeno"], dependencies=[Depends(auth)])
    def delete_folder(folder: Folder):
        delete.folder(folder)

    @api_app.delete("/tag", tags=["zeno"], dependencies=[Depends(auth)])
    def delete_tag(tag: Tag):
        delete.tag(tag)

    @api_app.delete("/organization", tags=["zeno"], dependencies=[Depends(auth)])
    def delete_organization(organization: Organization):
        delete.organization(organization)

    @api_app.delete(
        "/project_user/{project}", tags=["zeno"], dependencies=[Depends(auth)]
    )
    def delete_project_user(project: str, user: User):
        delete.project_user(project, user)

    @api_app.delete(
        "/project_org/{project}", tags=["zeno"], dependencies=[Depends(auth)]
    )
    def delete_project_org(project: str, organization: Organization):
        delete.project_org(project, organization)

    return app


def serve():
    """Serve the FastAPI application for the backend."""
    app = get_server()
    uvicorn.run(
        app,
        host=os.environ["BACKEND_HOST"] if "BACKEND_HOST" in os.environ else "0.0.0.0",
        port=int(os.environ["BACKEND_PORT"]) if "BACKEND_PORT" in os.environ else 80,
    )
