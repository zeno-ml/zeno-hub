"""FastAPI server endpoints for metadata-related queries."""
import asyncio
import datetime

from fastapi import (
    APIRouter,
    HTTPException,
    Request,
    status,
)

import zeno_backend.database.select as select
import zeno_backend.util as util
from zeno_backend.classes.base import (
    ZenoColumn,
)
from zeno_backend.classes.homepage import EntryTypeFilter, HomeEntry, HomeRequest
from zeno_backend.classes.metadata import HistogramBucket, StringFilterRequest
from zeno_backend.processing.filtering import table_filter
from zeno_backend.processing.histogram_processing import (
    HistogramRequest,
    histogram_metric_and_count,
)

router = APIRouter(tags=["zeno"])


@router.get(
    "/models/{project}",
    response_model=list[str],
    tags=["zeno"],
)
def get_models(project_uuid: str, request: Request):
    """Get all models for a project.

    Args:
        project_uuid (str): project to get the models for.
        request (Request): http request to get user information from.

    Returns:
        list[str]: all models associated with a project.
    """
    util.project_access_valid(project_uuid, request)
    return select.models(project_uuid)


@router.get(
    "/columns/{project_uuid}",
    response_model=list[ZenoColumn],
    tags=["zeno"],
)
def get_columns(project_uuid: str, request: Request):
    """Get all columns of a project.

    Args:
        project_uuid (str): UUID of the project to get all columns for.
        request (Request): http request to get user information from.

    Returns:
        list[ZenoColumn]: all columns associated with a project.
    """
    util.project_access_valid(project_uuid, request)
    return select.columns(project_uuid)


@router.post(
    "/home-details",
    response_model=list[HomeEntry],
    tags=["zeno"],
)
def get_home_details(home_request: HomeRequest, req: Request):
    """Get the details of the home view including projects, reports, and statistics.

    Args:
        home_request (HomeRequest): request specification for the home view.
        req (Request): http request to get user information from.

    Returns:
        list[HomeEntry]: list of all entries in the home view that match the request.
    """
    user = util.get_user_from_token(req)
    if user is None and home_request.user_name is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not logged in",
        )

    if (
        home_request.type_filter != EntryTypeFilter.PROJECT
        and home_request.type_filter != EntryTypeFilter.ALL
    ):
        projects = []
    elif user and home_request.user_name is not None:
        projects = select.projects(user, home_request)
    else:
        projects = select.public_projects(home_request)
    project_ret: list[HomeEntry] = []
    for proj in projects:
        stats = select.project_stats(proj.uuid, user.id if user else None)
        project_ret.append(HomeEntry(entry=proj, stats=stats))

    if (
        home_request.type_filter != EntryTypeFilter.REPORT
        and home_request.type_filter != EntryTypeFilter.ALL
    ):
        reports = []
    elif user and home_request.user_name is not None:
        reports = select.reports(user, home_request)
    else:
        reports = select.public_reports(home_request)
    report_ret: list[HomeEntry] = []
    for rep in reports:
        stats = select.report_stats(rep.id, user.id if user else None)
        report_ret.append(HomeEntry(entry=rep, stats=stats))

    return_entries = project_ret + report_ret

    if home_request.sort == "POPULAR":
        return_entries.sort(key=lambda x: x.stats.num_likes, reverse=True)
    elif home_request.sort == "RECENT":
        return_entries.sort(
            key=lambda x: datetime.datetime.fromisoformat(x.entry.updated_at),
            reverse=True,
        )

    # Make sure the combined entries don't exceed the number of requested items
    if home_request.limit is not None:
        return_entries = return_entries[: home_request.limit]

    return return_entries


@router.post(
    "/histograms/{project_uuid}",
    response_model=list[list[HistogramBucket]],
    tags=["zeno"],
)
async def calculate_histograms(
    req: HistogramRequest, project_uuid: str, request: Request
):
    """Calculate the histograms for a project.

    Args:
        req (HistogramRequest): specification of te histogram request.
        project_uuid (str): UUID of the project to calculate histograms for.
        request (Request): http request to get user information from.

    Returns:
        list[list[HistogramBucket]]: histogram buckets for all requested histograms.
    """
    util.project_access_valid(project_uuid, request)

    project_obj = select.project_from_uuid(project_uuid)
    if project_obj is None:
        return []

    filter_sql = table_filter(
        project_uuid, req.model, req.filter_predicates, req.data_ids
    )

    # get buckets or generate if not exist.
    histograms = await select.histogram_buckets(project_uuid, req.columns)
    if histograms is None:
        return []

    res = await asyncio.gather(
        *[
            histogram_metric_and_count(
                req,
                col,
                histograms[col.id],
                project_uuid,
                filter_sql,
            )
            for col in req.columns
        ]
    )
    return res


@router.post(
    "/string-filter/{project}",
    response_model=list[str],
    tags=["zeno"],
)
def filter_string_metadata(project: str, req: StringFilterRequest, request: Request):
    """Select distinct string values of a column and return their short representation.

    Args:
        project (str): the project for which to filter the column
        req (StringFilterRequest): the specification of the filter operation.
        request (Request): http request to get user information from.

    Returns:
        list[str]: the filtered string column data.
    """
    util.project_access_valid(project, request)
    return select.filtered_short_string_column_values(project, req)
