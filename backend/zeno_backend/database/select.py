"""Functions to select data from the database."""
import json
from operator import itemgetter
from typing import List, Optional, Union

from psycopg import DatabaseError, sql

from zeno_backend.classes.base import ProjectConfig, ZenoColumn
from zeno_backend.classes.chart import Chart
from zeno_backend.classes.filter import FilterPredicateGroup, Join
from zeno_backend.classes.folder import Folder
from zeno_backend.classes.metric import Metric
from zeno_backend.classes.slice import Slice
from zeno_backend.classes.slice_finder import SQLTable
from zeno_backend.classes.tag import Tag
from zeno_backend.database.database import Database


def models(project: str) -> List[str]:
    """Get all models for a specified project.

    Args:
        project (str): the project the user is currently working with.

    Returns:
        List[str]: a list of model names included in the project.
    """
    db = Database()
    model_results = db.connect_execute_return(
        sql.SQL("SELECT DISTINCT model FROM {} WHERE model IS NOT NULL;").format(
            sql.Identifier(f"{project}_column_map")
        ),
        return_all=True,
    )
    return list(map(itemgetter(0), model_results)) if model_results is not None else []


def projects() -> List[ProjectConfig]:
    """Get all projects available to the user.

    Returns:
        List[ProjectConfig]: the projects that the user can interact with.
    """
    db = Database()
    project_result = db.connect_execute_return(
        "SELECT uuid, name, view, calculate_histogram_metrics, num_items "
        "FROM projects;",
        return_all=True,
    )
    return (
        list(
            map(
                lambda project: ProjectConfig(
                    uuid=project[0],
                    name=project[1],
                    view=project[2],
                    calculate_histogram_metrics=bool(project[3]),
                    num_items=project[4],
                ),
                project_result,
            )
        )
        if project_result is not None
        else []
    )


def project(project: str) -> Union[ProjectConfig, None]:
    """Get the project data for a specific project ID.

    Args:
        project (str): the project the user is currently working with.

    Returns:
        Union[ProjectConfig, None]: the data for the requested project.
    """
    db = Database()
    project_result = db.connect_execute_return(
        "SELECT uuid, name, view, calculate_histogram_metrics, num_items FROM projects "
        "WHERE uuid = %s",
        [
            project,
        ],
    )
    return (
        ProjectConfig(
            uuid=str(project_result[0]),
            name=str(project_result[1]),
            view=str(project_result[2]),
            calculate_histogram_metrics=bool(project_result[3]),
            num_items=project_result[4] if isinstance(project_result[4], int) else 5,
        )
        if project_result is not None
        else None
    )


def metrics(project: str) -> List[Metric]:
    """Get a list of all metrics that are used in the project.

    Args:
        project (str): the project the user is currently working with.

    Returns:
        List[Metric]: list of metrics used with the project.
    """
    db = Database()
    metric_results = db.connect_execute_return(
        "SELECT metrics.id, metrics.name FROM metrics INNER JOIN project_metrics ON "
        "metrics.id = project_metrics.metric_id "
        "WHERE project_metrics.project_uuid = %s;",
        [
            project,
        ],
        return_all=True,
    )
    return (
        list(map(lambda metric: Metric(id=metric[0], name=metric[1]), metric_results))
        if metric_results is not None
        else []
    )


def folders(project: str) -> List[Folder]:
    """Get a list of all folders in a project.

    Args:
        project (str): the project the user is currently working with.

    Returns:
        List[Folder]: list of folders created in the project.
    """
    db = Database()
    folder_results = db.connect_execute_return(
        "SELECT id, name, project_uuid FROM folders WHERE project_uuid = %s;",
        [
            project,
        ],
        return_all=True,
    )
    return (
        list(
            map(
                lambda folder: Folder(id=folder[0], name=folder[1]),
                folder_results,
            )
        )
        if folder_results is not None
        else []
    )


def folder(id: int) -> Union[Folder, None]:
    """Get a single folder by its ID.

    Args:
        id (int): id of the folder to be fetched.

    Returns:
        Union[Folder, None]: Folder as requested by the user.
    """
    db = Database()
    folder_result = db.connect_execute_return(
        "SELECT id, name, project_uuid FROM folders WHERE id = %s;",
        [
            id,
        ],
    )
    return (
        Folder(
            id=folder_result[0] if isinstance(folder_result[0], int) else 0,
            name=str(folder_result[1]),
        )
        if folder_result is not None
        else None
    )


def slices(project: str, ids: Optional[List[int]] = None) -> List[Slice]:
    """Get a list of all slices of a project with certain IDs.

    Args:
        project (str): the project the user is currently working with.
        ids (Optional[List[int]], optional): Limited list of slice IDs to fetch from,
        using all slices of the project if None. Defaults to None.

    Returns:
        List[Slice]: List of requested slices.
    """
    if ids is not None and len(ids) == 0:
        return []
    db = Database()
    if ids is None:
        slice_results = db.connect_execute_return(
            "SELECT id, name, folder_id, filter FROM slices WHERE project_uuid = %s;",
            [
                project,
            ],
            return_all=True,
        )
    else:
        slice_results = db.connect_execute_return(
            "SELECT id, name, folder_id, filter FROM slices "
            "WHERE project_uuid = %s AND id = ANY(%s);",
            [
                project,
                ids,
            ],
            return_all=True,
        )
    return (
        list(
            map(
                lambda slice: Slice(
                    id=slice[0],
                    slice_name=slice[1],
                    folder_id=slice[2],
                    filter_predicates=FilterPredicateGroup(
                        predicates=json.loads(slice[3])["predicates"],
                        join=Join.OMITTED,
                    ),
                ),
                slice_results,
            )
        )
        if slice_results is not None
        else []
    )


def charts(project: str) -> List[Chart]:
    """Get a list of all charts created in the project.

    Args:
        project (str): the project the user is currently working with.

    Returns:
        List[Chart]: list of all the charts in the project.
    """
    db = Database()
    chart_results = db.connect_execute_return(
        "SELECT id, name, type, parameters FROM charts WHERE project_uuid = %s;",
        [
            project,
        ],
        return_all=True,
    )
    return (
        list(
            map(
                lambda chart: Chart(
                    id=chart[0],
                    name=chart[1],
                    type=chart[2],
                    parameters=json.loads(chart[3]),
                ),
                chart_results,
            )
        )
        if chart_results is not None
        else []
    )


def columns(project: str) -> List[ZenoColumn]:
    """Get a list of all columns in the project's data table.

    Args:
        project (str): the project the user is currently working with.

    Returns:
        List[ZenoColumn]: list of all the project's data columns.
    """
    db = Database()
    column_results = db.connect_execute_return(
        sql.SQL("SELECT column_id, name, type, model, data_type FROM {};").format(
            sql.Identifier(f"{project}_column_map")
        ),
        return_all=True,
    )
    return (
        (
            list(
                map(
                    lambda column: ZenoColumn(
                        id=column[0],
                        name=column[1],
                        column_type=column[2],
                        model=column[3],
                        data_type=column[4],
                    ),
                    column_results,
                )
            )
        )
        if column_results is not None
        else []
    )


def table_data_paginated(
    project: str, filter_sql: Optional[sql.Composed], offset: int, limit: int
) -> SQLTable:
    """Get a slice of the data saved in the project table.

    Args:
        project (str): the project the user is currently working with.
        filter_sql (Optional[sql.Composed]): filter to apply before fetching a slice of
        the data.
        offset (int): where in the remaining data to start extracting the slice.
        limit (int): maximum slice length to be extracted.

    Raises:
        Exception: something failed while reading the data from the database.

    Returns:
        SQLTable: the resulting slice of the data as requested by the user.
    """
    db = Database()
    try:
        filter_results = None
        columns = []
        db.connect()
        if filter_sql is None:
            if db.cur is not None:
                db.cur.execute(
                    sql.SQL(
                        "SELECT * FROM {} ORDER BY item LIMIT %s OFFSET %s;"
                    ).format(sql.Identifier(f"{project}")),
                    [
                        limit,
                        offset,
                    ],
                )
                if db.cur.description is not None:
                    columns = [desc[0] for desc in db.cur.description]
                filter_results = db.cur.fetchall()
        else:
            if db.cur is not None:
                db.cur.execute(
                    sql.SQL("SELECT * FROM {} WHERE ").format(sql.Identifier(project))
                    + filter_sql
                    + sql.SQL("ORDER BY item LIMIT {} OFFSET {};").format(
                        sql.Literal(limit), sql.Literal(offset)
                    )
                )
                if db.cur.description is not None:
                    columns = [desc[0] for desc in db.cur.description]
                filter_results = db.cur.fetchall()
        return (
            SQLTable(table=filter_results, columns=columns)
            if filter_results is not None
            else SQLTable(table=[], columns=[])
        )
    except (Exception, DatabaseError) as error:
        raise Exception(error) from error
    finally:
        db.disconnect()


def table_data(project: str, filter_sql: Optional[sql.Composed]) -> SQLTable:
    """Get the filtered data table for the current project.

    Args:
        project (str): the project the user is currently working with.
        filter_sql (Optional[sql.Composed]): filters to apply to the fetched data.

    Raises:
        Exception: something failed while reading the data from the database.

    Returns:
        SQLTable: the filtered data table for the project.
    """
    db = Database()
    try:
        filter_results = None
        columns = []
        db.connect()
        if filter_sql is None:
            if db.cur is not None:
                db.cur.execute(
                    sql.SQL("SELECT * FROM {};").format(sql.Identifier(f"{project}")),
                )
                if db.cur.description is not None:
                    columns = [desc[0] for desc in db.cur.description]
                filter_results = db.cur.fetchall()
        else:
            if db.cur is not None:
                db.cur.execute(
                    sql.SQL("SELECT * FROM {} WHERE ").format(sql.Identifier(project))
                    + filter_sql
                )
                if db.cur.description is not None:
                    columns = [desc[0] for desc in db.cur.description]
                filter_results = db.cur.fetchall()
        return (
            SQLTable(table=filter_results, columns=columns)
            if filter_results is not None
            else SQLTable(table=[], columns=[])
        )
    except (Exception, DatabaseError) as error:
        raise Exception(error) from error
    finally:
        db.disconnect()


def column_id_from_name_and_model(project: str, column_name: str, model: str) -> str:
    """Get a column's id given its name and model.

    Args:
        project (str): the project the user is currently working with.
        column_name (str): the name of the column to be fetched.
        model (str): the model of the column to be fetched.

    Returns:
        str: _description_
    """
    db = Database()
    column_result = db.connect_execute_return(
        sql.SQL(
            "SELECT column_id FROM {} "
            "WHERE name = %s AND (model = %s OR model IS NULL);"
        ).format(sql.Identifier(f"{project}_column_map")),
        [column_name, model],
    )
    return str(column_result[0]) if column_result is not None else ""


def column(
    project: str, column: ZenoColumn, filter_sql: Optional[sql.Composed] = None
) -> List[Union[str, int, float, bool]]:
    """Get the data for one column of the project's data table.

    Args:
        project (str): the project the user is currently working with.
        column (ZenoColumn): the column for which to fetch the data.
        filter_sql (Optional[sql.Composed], optional): Any filters to apply before
        fetching the column data. Defaults to None.

    Returns:
        List[Union[str, int, float, bool]]: the data that is stored in the requested
        column.
    """
    db = Database()
    if filter_sql is None:
        column_result = db.connect_execute_return(
            sql.SQL("SELECT {} FROM {}").format(
                sql.Identifier(column.id), sql.Identifier(project)
            ),
            return_all=True,
        )
    else:
        column_result = db.connect_execute_return(
            sql.SQL("SELECT {} FROM {} WHERE ").format(
                sql.Identifier(column.id), sql.Identifier(project)
            )
            + filter_sql,
            return_all=True,
        )
    return (
        list(map(lambda column: column[0], column_result))
        if column_result is not None
        else []
    )


def tags(project: str) -> List[Tag]:
    """Get a list of all tags created for a project.

    Args:
        project (str): the project the user is currently working with.

    Raises:
        Exception: something went wrong while extracting the tags from the database.

    Returns:
        List[Tag]: the list of tags associated with a project.
    """
    db = Database()
    try:
        db.connect()
        tags_result = db.execute_return(
            "SELECT id, name, folder_id FROM tags WHERE project_uuid = %s",
            [
                project,
            ],
            return_all=True,
        )
        if tags_result is None:
            return []
        tags: List[Tag] = []
        for tag_result in tags_result:
            items_result = db.execute_return(
                sql.SQL("SELECT item_id FROM {} WHERE tag_id = %s").format(
                    sql.Identifier(f"{project}_tags_items")
                ),
                [
                    tag_result[0],
                ],
                return_all=True,
            )
            tags.append(
                Tag(
                    id=tag_result[0],
                    tag_name=tag_result[1],
                    folder_id=tag_result[2],
                    items=[]
                    if items_result is None
                    else list(map(lambda item: item[0], items_result)),
                )
            )
        return tags
    except (Exception, DatabaseError) as error:
        raise Exception(error) from error
    finally:
        db.disconnect()


def secret(email: str) -> Optional[str]:
    """Get the secret of a user with a specific email address.

    Args:
        email (str): the email address of the user for which to fetch the secret.

    Returns:
        Optional[str]: the secret of the user.
    """
    db = Database()
    secret = db.connect_execute_return(
        "SELECT secret FROM users WHERE email = %s", [email]
    )
    if secret is None:
        return None
    return str(secret[0])
