"""FastAPI server endpoints for data-table-related queries."""
import pandas as pd
from fastapi import APIRouter, HTTPException, Request, status

import zeno_backend.database.select as select
import zeno_backend.util as util
from zeno_backend.classes.table import SliceTableRequest, TableRequest, TagTableRequest
from zeno_backend.processing.filtering import table_filter

router = APIRouter(tags=["zeno"])


@router.post(
    "/filtered-table/{project_uuid}",
    response_model=str,
    tags=["zeno"],
)
async def get_filtered_table(req: TableRequest, project_uuid: str, request: Request):
    """Get the data in a project's table.

    Args:
        req (TableRequest): specification of the data request to the table.
        project_uuid (str): project to fetch data for.
        request (Request): http request to get user information from.

    Returns:
        json: json representation of the requested data.
    """
    await util.project_access_valid(project_uuid, request)
    filter_sql = await table_filter(
        project_uuid, req.model, req.filter_predicates, req.data_ids
    )

    sql_table = await select.table_data_paginated(project_uuid, filter_sql, req)
    table = pd.DataFrame(sql_table.table, columns=sql_table.columns)

    return table.to_json(orient="records")


@router.post(
    "/slice-table",
    response_model=str,
    tags=["zeno"],
)
async def get_slice_table(slice_table_request: SliceTableRequest, request: Request):
    """Get the data in a project's table for a specific slice.

    Args:
        slice_table_request (SliceTableRequest): specification of the data request.
        request (Request): http request to get user information from.

    Raises:
        HTTPException: error if the data cannot be loaded.

    Returns:
        json: json representation of the requested data.
    """
    slice = await select.slice(slice_table_request.slice_id)
    project_uuid = slice.project_uuid
    if project_uuid is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    await util.project_access_valid(project_uuid, request)

    filter_sql = await table_filter(
        project_uuid, slice_table_request.model, slice.filter_predicates
    )

    sql_table = await select.slice_or_tag_table(
        project_uuid, filter_sql, slice_table_request
    )

    table = pd.DataFrame(sql_table.table, columns=sql_table.columns)
    return table.to_json(orient="records")


@router.post(
    "/tag-table",
    response_model=str,
    tags=["zeno"],
)
async def get_tag_table(tag_table_request: TagTableRequest, request: Request):
    """Get the data in a project's table for a specific tag.

    Args:
        tag_table_request (TagTableRequest): specification of the data request.
        request (Request): http request to get user information from.

    Raises:
        HTTPException: errorr if the data cannot be loaded.

    Returns:
        json: json representation of the requested data.
    """
    tag = await select.tag(tag_table_request.tag_id)
    project_uuid = tag.project_uuid
    if project_uuid is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    await util.project_access_valid(project_uuid, request)

    filter_sql = await table_filter(
        project_uuid, tag_table_request.model, data_ids=tag.data_ids
    )

    sql_table = await select.slice_or_tag_table(
        project_uuid, filter_sql, tag_table_request
    )

    table = pd.DataFrame(sql_table.table, columns=sql_table.columns)
    return table.to_json(orient="records")
