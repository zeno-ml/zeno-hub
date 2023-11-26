"""Functions to select data from the database."""
import asyncio
import json

from fastapi import HTTPException, status
from psycopg import sql

from zeno_backend.classes.base import MetadataType, ZenoColumn, ZenoColumnType
from zeno_backend.classes.chart import Chart
from zeno_backend.classes.filter import FilterPredicateGroup, Join, Operation
from zeno_backend.classes.folder import Folder
from zeno_backend.classes.homepage import EntrySort, HomeRequest
from zeno_backend.classes.metadata import HistogramBucket, StringFilterRequest
from zeno_backend.classes.metric import Metric
from zeno_backend.classes.project import (
    Project,
    ProjectState,
    ProjectStats,
)
from zeno_backend.classes.report import (
    Report,
    ReportElement,
    ReportResponse,
    ReportStats,
    SliceElementOptions,
    TagElementOptions,
)
from zeno_backend.classes.slice import Slice
from zeno_backend.classes.slice_finder import SQLTable
from zeno_backend.classes.table import (
    SliceTableRequest,
    TableRequest,
    TagTableRequest,
)
from zeno_backend.classes.tag import Tag
from zeno_backend.classes.user import Organization, User
from zeno_backend.database.database import Database, db_pool
from zeno_backend.database.util import hash_api_key, match_instance_view
from zeno_backend.processing.filtering import table_filter
from zeno_backend.processing.histogram_processing import calculate_histogram_bucket

PROJECTS_BASE_QUERY = sql.SQL(
    """
    (SELECT main.*, u.name AS owner_name FROM (
        SELECT p.uuid, p.name, p.owner_id, p.view, p.samples_per_page,
        p.public, p.description, TRUE AS editor, p.created_at, p.updated_at
        FROM projects AS p
        WHERE p.owner_id = %s
        
        UNION

        SELECT p.uuid, p.name, p.owner_id, p.view, p.samples_per_page,
            p.public, p.description, up.editor, p.created_at, p.updated_at
        FROM projects AS p
        LEFT JOIN user_project AS up ON p.uuid = up.project_uuid
        WHERE up.user_id = %s AND p.owner_id != %s

        UNION

        SELECT p.uuid, p.name, p.owner_id, p.view, p.samples_per_page,
            p.public, p.description, op.editor, p.created_at, p.updated_at
        FROM projects AS p 
        JOIN (SELECT op.project_uuid, uo.organization_id, editor
                FROM user_organization AS uo
                JOIN organization_project AS op
                ON uo.organization_id = op.organization_id
                WHERE uo.user_id = %s) AS op ON p.uuid = op.project_uuid
        WHERE p.owner_id != %s) AS main 
    LEFT JOIN users AS u ON main.owner_id = u.id)
    """
)

REPORTS_BASE_QUERY = sql.SQL(
    """
    (SELECT main.*, u.name AS owner_name FROM (
        SELECT r.id, r.name, r.owner_id, r.public, r.description, TRUE AS editor,
        r.created_at, r.updated_at FROM reports AS r
        WHERE r.owner_id = %s

        UNION

        SELECT r.id, r.name, r.owner_id, r.public, r.description, ur.editor,
        r.created_at, r.updated_at FROM reports AS r
        LEFT JOIN user_report AS ur ON r.id = ur.report_id
        WHERE ur.user_id = %s AND r.owner_id != %s

        UNION

        SELECT r.id, r.name, r.owner_id, r.public, r.description, orr.editor,
        r.created_at, r.updated_at FROM reports AS r 
        JOIN (SELECT orr.report_id, uo.organization_id, editor
                FROM user_organization AS uo
                JOIN organization_report AS orr
                ON uo.organization_id = orr.organization_id
                WHERE uo.user_id = %s) AS orr ON r.id = orr.report_id
        WHERE r.owner_id != %s) AS main
    LEFT JOIN users AS u ON main.owner_id = u.id)
    """
)


def models(project: str) -> list[str]:
    """Get all models for a specified project.

    Args:
        project (str): the project the user is currently working with.

    Returns:
        list[str]: a list of model names included in the project.
    """
    db = Database()
    model_results = db.connect_execute_return(
        sql.SQL("SELECT DISTINCT model FROM {} WHERE model IS NOT NULL;").format(
            sql.Identifier(f"{project}_column_map")
        ),
    )
    return [m[0] for m in model_results]


def projects(user: User, home_request: HomeRequest) -> list[Project]:
    """Get all projects available to the user.

    Args:
        user (User): the user for which to fetch the available projects.
        home_request (ProjectsRequest): the request object.

    Returns:
        list[Project]: the projects that the user can interact with.
    """
    with Database() as db:
        params = [user.id, user.id, user.id, user.id, user.id]
        likes_query = sql.SQL(
            "SELECT project_uuid, COUNT(*) as total_likes"
            " FROM project_like GROUP BY project_uuid "
        )
        projects_query = (
            sql.SQL("WITH LikesSummary AS (")
            + likes_query
            + sql.SQL("),")
            + sql.SQL(" CombinedProjects AS (")
            + PROJECTS_BASE_QUERY
            + sql.SQL(") ")
            + sql.SQL(
                "SELECT cp.*, COALESCE(ls.total_likes, 0) AS total_likes FROM"
                " CombinedProjects cp LEFT JOIN LikesSummary ls "
                " ON cp.uuid = ls.project_uuid "
            )
        )

        if home_request.search_string:
            projects_query += sql.SQL(
                "WHERE (LOWER(cp.name) LIKE LOWER(%s) OR "
                "LOWER(cp.description) LIKE LOWER(%s)) "
            )
            params += [
                "%" + home_request.search_string + "%",
                "%" + home_request.search_string + "%",
            ]

        if home_request.sort == EntrySort.POPULAR:
            projects_query += sql.SQL(" ORDER BY total_likes DESC, updated_at DESC ")
        elif home_request.sort == EntrySort.RECENT:
            projects_query += sql.SQL(" ORDER BY updated_at DESC ")

        if home_request.limit:
            projects_query += sql.SQL(" LIMIT %s ")
            params += [home_request.limit]
        projects_query += sql.SQL(" OFFSET %s; ")
        params += [home_request.project_offset]

        projects_result = db.execute_return(projects_query, params)

        projects = []
        for res in projects_result:
            projects.append(
                Project(
                    uuid=res[0],
                    name=res[1],
                    view=match_instance_view(res[3]),
                    samples_per_page=res[4],
                    public=res[5],
                    description=res[6],
                    editor=res[7],
                    created_at=res[8].isoformat(),
                    updated_at=res[9].isoformat(),
                    owner_name=res[10],
                )
            )
        return projects


def public_projects(home_request: HomeRequest) -> list[Project]:
    """Fetch all publicly accessible projects.

    Args:
        home_request (ProjectsRequest): the request object.

    Returns:
        list[Project]: all publicly accessible projects.
    """
    with Database() as db:
        params = []
        projects_query = sql.SQL(
            "SELECT p.uuid, p.name, p.owner_id, p.view, p.samples_per_page, "
            "p.description, p.public, p.created_at, p.updated_at, "
            "COALESCE(ls.total_likes, 0) AS total_likes "
            "FROM projects AS p "
            "LEFT JOIN (SELECT project_uuid, COUNT(*) as total_likes "
            "FROM project_like GROUP BY project_uuid) AS ls "
            "ON p.uuid = ls.project_uuid "
            "WHERE p.public IS TRUE "
        )
        if home_request.search_string:
            projects_query += sql.SQL(
                "AND (LOWER(p.name) LIKE LOWER(%s) OR "
                "LOWER(p.description) LIKE LOWER(%s)) "
            )
            params += [
                "%" + home_request.search_string + "%",
                "%" + home_request.search_string + "%",
            ]

        if home_request.sort == EntrySort.POPULAR:
            projects_query += sql.SQL(" ORDER BY total_likes DESC, updated_at DESC ")
        elif home_request.sort == EntrySort.RECENT:
            projects_query += sql.SQL(" ORDER BY updated_at DESC ")

        if home_request.limit:
            projects_query += sql.SQL(" LIMIT %s ")
            params += [home_request.limit]
        projects_query += sql.SQL(" OFFSET %s")
        params += [home_request.project_offset]

        projects_query = (
            sql.SQL("(SELECT main.*, u.name AS owner_name FROM (")
            + projects_query
            + sql.SQL(") AS main LEFT JOIN users AS u ON main.owner_id = u.id)")
        )

        projects_result = db.execute_return(projects_query, params)

        projects = []
        for res in projects_result:
            projects.append(
                Project(
                    uuid=res[0],
                    name=res[1],
                    view=match_instance_view(res[3]),
                    samples_per_page=res[4],
                    editor=False,
                    public=True,
                    description=res[5],
                    created_at=res[7].isoformat(),
                    updated_at=res[8].isoformat(),
                    owner_name=res[10],
                )
            )
        return projects


def reports(user: User, home_request: HomeRequest) -> list[Report]:
    """Get all reports available to the user.

    Args:
        user (User): the user for which to fetch the available reports.
        home_request (HomeRequest): the request object.

    Returns:
        list[Report]: the reports that the user can interact with.
    """
    with Database() as db:
        params = [user.id, user.id, user.id, user.id, user.id]
        likes_query = sql.SQL(
            "SELECT report_id, COUNT(*) as total_likes"
            " FROM report_like GROUP BY report_id "
        )
        reports_query = (
            sql.SQL("WITH LikesSummary AS (")
            + likes_query
            + sql.SQL("),")
            + sql.SQL(" CombinedReports AS (")
            + REPORTS_BASE_QUERY
            + sql.SQL(") ")
            + sql.SQL(
                "SELECT cp.*, COALESCE(ls.total_likes, 0) AS total_likes FROM"
                " CombinedReports cp LEFT JOIN LikesSummary ls "
                " ON cp.id = ls.report_id "
            )
        )

        if home_request.search_string:
            reports_query += sql.SQL(
                "WHERE (LOWER(cp.name) LIKE LOWER(%s) OR "
                "LOWER(cp.description) LIKE LOWER(%s)) "
            )
            params += [
                "%" + home_request.search_string + "%",
                "%" + home_request.search_string + "%",
            ]

        if home_request.sort == EntrySort.POPULAR:
            reports_query += sql.SQL(" ORDER BY total_likes DESC, updated_at DESC ")
        elif home_request.sort == EntrySort.RECENT:
            reports_query += sql.SQL(" ORDER BY updated_at DESC ")

        if home_request.limit:
            reports_query += sql.SQL(" LIMIT %s ")
            params += [home_request.limit]
        reports_query += sql.SQL(" OFFSET %s; ")
        params += [home_request.report_offset]

        reports_result = db.execute_return(reports_query, params)

        reports = []
        for report in reports_result:
            linked_projects = db.execute_return(
                "SELECT project_uuid FROM report_project WHERE report_id = %s;",
                [report[0]],
            )
            reports.append(
                Report(
                    id=report[0],
                    name=report[1],
                    linked_projects=[]
                    if len(linked_projects) == 0
                    else list(map(lambda linked: str(linked[0]), linked_projects)),
                    public=report[3],
                    description=report[4],
                    editor=report[5],
                    created_at=report[6].isoformat(),
                    updated_at=report[7].isoformat(),
                    owner_name=report[8],
                )
            )
        return reports


def public_reports(home_request: HomeRequest) -> list[Report]:
    """Fetch all publicly accessible reports.

    Args:
        home_request (HomeRequest): the request object.

    Returns:
        list[Report]: all publicly accessible reports.
    """
    with Database() as db:
        params = []
        reports_query = sql.SQL(
            "SELECT r.id, r.name, r.owner_id, r.description, r.public,"
            " r.created_at, r.updated_at, COALESCE(ls.total_likes, 0) AS total_likes "
            "FROM reports AS r "
            "LEFT JOIN (SELECT report_id, COUNT(*) as total_likes "
            "FROM report_like GROUP BY report_id) AS ls "
            "ON r.id = ls.report_id "
            "WHERE r.public IS TRUE "
        )
        if home_request.search_string:
            reports_query += sql.SQL(
                "AND (LOWER(r.name) LIKE LOWER(%s) OR "
                "LOWER(r.description) LIKE LOWER(%s)) "
            )
            params += [
                "%" + home_request.search_string + "%",
                "%" + home_request.search_string + "%",
            ]

        if home_request.sort == EntrySort.POPULAR:
            reports_query += sql.SQL(" ORDER BY total_likes DESC, updated_at DESC ")
        elif home_request.sort == EntrySort.RECENT:
            reports_query += sql.SQL(" ORDER BY r.updated_at DESC ")

        if home_request.limit:
            reports_query += sql.SQL(" LIMIT %s ")
            params += [home_request.limit]
        reports_query += sql.SQL(" OFFSET %s")
        params += [home_request.report_offset]

        reports_query = (
            sql.SQL("SELECT main.*, u.name AS owner_name FROM (")
            + reports_query
            + sql.SQL(") AS main LEFT JOIN users AS u ON main.owner_id = u.id")
        )
        report_result = db.execute_return(reports_query, params)

        reports = []
        if report_result is not None:
            for res in report_result:
                linked_projects = db.execute_return(
                    "SELECT project_uuid FROM report_project WHERE report_id = %s;",
                    [res[0]],
                )
                reports.append(
                    Report(
                        id=res[0],
                        name=res[1],
                        linked_projects=[]
                        if len(linked_projects) == 0
                        else list(map(lambda linked: str(linked[0]), linked_projects)),
                        editor=False,
                        public=True,
                        description=res[3],
                        created_at=res[5].isoformat(),
                        updated_at=res[6].isoformat(),
                        owner_name=res[8],
                    )
                )
        return reports


def project_count(user: User | None = None) -> int:
    """Get the number of projects.

    Args:
        user (User | None): the user making the request.

    Returns:
        int: the number of projects.
    """
    db = Database()
    if user is None:
        res = db.connect_execute_return(
            "SELECT COUNT(*) FROM projects WHERE public = TRUE;"
        )
    else:
        res = db.connect_execute_return(
            sql.SQL("SELECT COUNT(*) FROM") + PROJECTS_BASE_QUERY + sql.SQL(";"),
            [user.id, user.id, user.id, user.id, user.id],
        )

    if len(res) > 0:
        return res[0][0]
    return 0


def report_count(user: User | None = None) -> int:
    """Get the number of reports.

    Args:
        user (User | None): the user making the request.

    Returns:
        int: the number of reports.
    """
    db = Database()
    if user is None:
        res = db.connect_execute_return(
            "SELECT COUNT(*) FROM reports WHERE public = TRUE;"
        )
    else:
        res = db.connect_execute_return(
            sql.SQL("SELECT COUNT(*) FROM") + REPORTS_BASE_QUERY + sql.SQL(";"),
            [user.id, user.id, user.id, user.id, user.id],
        )
    if len(res) > 0:
        return res[0][0]
    return 0


def project_uuid(owner_name: str, project_name: str) -> str:
    """Get the project uuid given an owner and project name.

    Args:
        owner_name (str): name of the owner of the project.
        project_name (str): name of the project.

    Returns:
        str | None: uuid of the requested project.
    """
    with Database() as db:
        owner_id = db.execute_return(
            "SELECT id FROM users WHERE name = %s;", [owner_name]
        )

        project_uuid = db.execute_return(
            "SELECT uuid FROM projects WHERE name = %s AND owner_id = %s;",
            [project_name, owner_id[0][0]],
        )
        if len(project_uuid) == 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="ERROR: Project not found.",
            )
        return str(project_uuid[0][0])


def project_public(project_uuid: str) -> bool:
    """Check whether a project is public.

    Args:
        project_uuid (str): UUID of the project to be checked.

    Returns:
        bool: whether the project is public.
    """
    db = Database()
    public = db.connect_execute_return(
        "SELECT public FROM projects WHERE uuid = %s;", [project_uuid]
    )
    return bool(public[0][0]) if len(public) > 0 else False


def report_public(report: int) -> bool:
    """Check whether a report is public.

    Args:
        report (int): ID of the report to be checked.

    Returns:
        bool: whether the report is public.
    """
    db = Database()
    public = db.connect_execute_return(
        "SELECT public FROM reports WHERE id = %s;", [report]
    )
    return bool(public[0][0]) if len(public) > 0 else False


def api_key_exists(api_key: str) -> bool:
    """Check whether an API key exists.

    Args:
        api_key (str): the API key to check for.

    Returns:
        bool: whether the API key exists.
    """
    db = Database()
    api_key_hash = hash_api_key(api_key)
    exists = db.connect_execute_return(
        "SELECT EXISTS(SELECT 1 FROM users WHERE api_key_hash = %s);", [api_key_hash]
    )
    if len(exists) > 0:
        return bool(exists[0][0])
    else:
        raise Exception("Error while checking whether API key exists.")


def user_by_api_key(api_key: str) -> User:
    """Get the user ID given an API key.

    Args:
        api_key (str): the API key to get the user ID for.


    Returns:
        int | None: the user ID of the user with the given API key.
    """
    db = Database()
    api_key_hash = hash_api_key(api_key)
    user_res = db.connect_execute_return(
        "SELECT id, name, cognito_id FROM users WHERE api_key_hash = %s;",
        [api_key_hash],
    )
    if len(user_res) == 1:
        return User(
            id=int(user_res[0][0]), name=str(user_res[0][1]), cognito_id=user_res[0][2]
        )
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="ERROR: Invalid API key. Double check your API key or generate"
        + " a new one at https://hub.zenoml.com/account.",
    )


def user_name_by_api_key(api_key: str) -> str | None:
    """Get the user name given an API key.

    Args:
        api_key (str): the API key to get the user name for.


    Returns:
        str | None: the user name of the user with the given API key.
    """
    db = Database()
    api_key_hash = hash_api_key(api_key)
    user_id = db.connect_execute_return(
        "SELECT name FROM users WHERE api_key_hash = %s;", [api_key_hash]
    )
    return user_id[0][0] if len(user_id) > 0 else None


def project_uuid_exists(project_uuid: str) -> bool:
    """Check whether a project exists.

    Args:
        project_uuid (str): the UUID of the project.

    Returns:
        bool: whether the project exists.
    """
    db = Database()
    exists = db.connect_execute_return(
        "SELECT * FROM projects WHERE uuid = %s;", [project_uuid]
    )
    if len(exists) > 0:
        return True
    return False


def project_exists(owner_id: int, project_name: str) -> bool:
    """Check whether a project exists.

    Args:
        owner_id (int): the ID of the owner of the project.
        project_name (str): name of the project.


    Returns:
        bool: whether the project exists.


    Raises:
        Exception: something went wrong while checking whether the project exists.
    """
    db = Database()
    exists = db.connect_execute_return(
        "SELECT EXISTS(SELECT 1 FROM projects " "WHERE name = %s AND owner_id = %s);",
        [project_name, owner_id],
    )
    if len(exists) > 0:
        return bool(exists[0][0])
    else:
        raise Exception("Error while checking whether project exists.")


def report_id(owner: str, name: str) -> int | None:
    """Get report ID given owner and name.

    Args:
        owner (str): the owner of the report.
        name (str): the name of the report.

    Returns:
        int | None: the ID of the report.
    """
    with Database() as db:
        owner_id = db.execute_return("SELECT id FROM users WHERE name = %s;", [owner])
        if len(owner_id) == 0:
            return
        id = db.execute_return(
            "SELECT id FROM reports WHERE name = %s AND owner_id = %s;",
            [name, owner_id[0][0]],
        )
        if len(id) > 0:
            return id[0][0]


def report_response(id: int, user: User | None) -> ReportResponse:
    """Get the report data given a report ID.

    Args:
        id (int): the id of the report to be fetched.
        user (User | None): user making the request.

    Returns:
        ReportResponse | None: the data for the requested report.
    """
    with Database() as db:
        report_result = db.execute_return(
            "SELECT id, name, owner_id, public, description, created_at, updated_at "
            "FROM reports WHERE id = %s;",
            [id],
        )
        if len(report_result) == 0:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "ERROR: Report could not be found.",
            )
        else:
            report_result = report_result[0]

        owner_name = db.execute_return(
            "SELECT name FROM users WHERE id = %s;", [report_result[2]]
        )
        if len(owner_name) == 0:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "ERROR: Could not fetch owner of project.",
            )
        else:
            owner_name = owner_name[0][0]

        if user is None:
            editor = False
        elif int(report_result[2]) == user.id:
            # Owners can always edit projects
            editor = True
        else:
            # Check whether the user or an org of the user have project edit rights
            user_editor = db.execute_return(
                "SELECT editor FROM user_report WHERE user_id = %s "
                "AND report_id = %s",
                [user.id, id],
            )
            org_editor = db.execute_return(
                "SELECT * FROM organization_report AS r JOIN user_organization "
                "AS o ON r.organization_id = o.organization_id "
                "WHERE r.report_id = %s AND o.user_id = %s AND r.editor = TRUE;",
                [id, user.id],
            )
            editor = len(org_editor) > 0 or (
                bool(user_editor[0][0]) if len(user_editor) > 0 else False
            )

        linked_projects = db.execute_return(
            "SELECT project_uuid FROM report_project WHERE report_id = %s;",
            [id],
        )

        element_result = db.execute_return(
            "SELECT id, type, data, position FROM report_elements "
            "WHERE report_id = %s ORDER BY position;",
            [id],
        )

        num_likes = db.execute_return(
            "SELECT COUNT(*) FROM report_like WHERE report_id = %s;", [id]
        )

        user_liked = False
        if user is not None:
            user_liked = db.execute_return(
                "SELECT EXISTS(SELECT 1 FROM report_like WHERE report_id = %s AND "
                "user_id = %s);",
                [id, user.id],
            )
            if len(user_liked) > 0:
                user_liked = bool(user_liked[0][0])
            else:
                user_liked = False

        return ReportResponse(
            report=Report(
                id=report_result[0],
                name=report_result[1],
                owner_name=owner_name,
                linked_projects=[]
                if len(linked_projects) == 0
                else list(map(lambda linked: str(linked[0]), linked_projects)),
                editor=editor,
                public=report_result[3],
                description=report_result[4],
                created_at=report_result[5].isoformat(),
                updated_at=report_result[6].isoformat(),
            ),
            report_elements=list(
                map(
                    lambda element: ReportElement(
                        id=element[0],
                        type=element[1],
                        data=element[2],
                        position=element[3],
                    ),
                    element_result,
                )
            ),
            num_likes=num_likes[0][0] if isinstance(num_likes[0][0], int) else 0,
            user_liked=user_liked,
        )


def charts_for_projects(project_uuids: list[str]) -> list[Chart]:
    """Get all charts for a list of projects.

    Args:
        project_uuids (list[str]): the list of project uuids.

    Returns:
        list[Chart]: the list of charts.
    """
    db = Database()
    chart_results = db.connect_execute_return(
        sql.SQL(
            "SELECT id, name, type, parameters, project_uuid"
            " FROM charts WHERE project_uuid IN ({})"
        ).format(sql.SQL(",").join(map(sql.Literal, project_uuids)))
    )

    if len(chart_results) == 0:
        return []

    return list(
        map(
            lambda r: Chart(
                id=r[0],
                name=r[1],
                type=r[2],
                parameters=json.loads(r[3]),
                project_uuid=r[4],
            ),
            chart_results,
        )
    )


def tags_for_projects(project_uuids: list[str]) -> list[Tag]:
    """Get all tags for a list of projects.

    Args:
        project_uuids (list[str]): the list of project uuids.

    Returns:
        list[Tag]: the list of tags.
    """
    db = Database()
    tag_results = db.connect_execute_return(
        sql.SQL(
            "SELECT id, name, folder_id, project_uuid"
            " FROM tags WHERE project_uuid IN ({})"
        ).format(sql.SQL(",").join(map(sql.Literal, project_uuids)))
    )

    if len(tag_results) == 0:
        return []

    return list(
        map(
            lambda r: Tag(
                id=r[0],
                tag_name=r[1],
                data_ids=[],
                folder_id=r[2],
                project_uuid=r[3],
            ),
            tag_results,
        )
    )


def slices_for_projects(project_uuids: list[str]) -> list[Slice]:
    """Get all slices for a list of projects.

    Args:
        project_uuids (list[str]): the list of project uuids.


    Returns:
        list[Slice]: the list of slices.
    """
    db = Database()
    slice_results = db.connect_execute_return(
        sql.SQL(
            "SELECT id, name, folder_id, filter, project_uuid"
            " FROM slices WHERE project_uuid IN ({})"
        ).format(sql.SQL(",").join(map(sql.Literal, project_uuids)))
    )

    if len(slice_results) == 0:
        return []

    return list(
        map(
            lambda r: Slice(
                id=r[0],
                slice_name=r[1],
                folder_id=r[2],
                filter_predicates=FilterPredicateGroup(
                    predicates=json.loads(r[3])["predicates"],
                    join=Join.OMITTED,
                ),
                project_uuid=r[4],
            ),
            slice_results,
        )
    )


def project_from_uuid(project_uuid: str) -> Project:
    """Get the project data given a UUID.

    Args:
        project_uuid (str): the uuid of the project to be fetched.

    Returns:
        Project | None: data for the requested project.
    """
    with Database() as db:
        project_result = db.execute_return(
            "SELECT uuid, name, owner_id, view, "
            "samples_per_page, public, description, created_at, updated_at "
            "FROM projects WHERE uuid = %s;",
            [project_uuid],
        )
        if len(project_result) == 0:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "ERROR: Project could not be found.",
            )
        project_result = project_result[0]
        owner_result = db.execute_return(
            "SELECT name from users WHERE id = %s;", [project_result[2]]
        )
        if len(owner_result) > 0:
            return Project(
                uuid=str(project_result[0]),
                name=str(project_result[1]),
                owner_name=str(owner_result[0][0]),
                view=match_instance_view(str(project_result[3])),
                editor=False,
                samples_per_page=project_result[4]
                if isinstance(project_result[4], int)
                else 10,
                public=bool(project_result[5]),
                description=str(project_result[6]),
                created_at=project_result[7].isoformat(),
                updated_at=project_result[8].isoformat(),
            )
        else:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "ERROR: Could not load project owner.",
            )


def report_from_id(report_id: int) -> Report:
    """Get the report data given a ID.

    Args:
        report_id (int): the id of the report to be fetched.

    Returns:
        Report | None: data for the requested report.
    """
    with Database() as db:
        report_result = db.execute_return(
            "SELECT id, name, owner_id, public, description, created_at, updated_at "
            "FROM reports WHERE id = %s;",
            [report_id],
        )
        if len(report_result) == 0:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "ERROR: Report could not be found.",
            )
        else:
            report_result = report_result[0]
        owner_result = db.execute_return(
            "SELECT name FROM users WHERE id = %s;", [report_result[2]]
        )
        if len(owner_result) > 0:
            linked_projects = db.execute_return(
                "SELECT project_uuid FROM report_project WHERE report_id = %s;",
                [report_id],
            )
            owner_result = owner_result[0]

            return Report(
                id=report_result[0] if isinstance(report_result[0], int) else -1,
                name=str(report_result[1]),
                owner_name=str(owner_result[0]),
                linked_projects=[]
                if len(linked_projects) == 0
                else list(map(lambda linked: str(linked[0]), linked_projects)),
                editor=False,
                public=bool(report_result[3]),
                description=str(report_result[4]),
                created_at=report_result[5].isoformat(),
                updated_at=report_result[6].isoformat(),
            )
        else:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "ERROR: Could not load report owner.",
            )


def report_elements(report_id: int) -> list[ReportElement] | None:
    """Get all elements of a report.

    Args:
        report_id (int): the id of the report to get elements for.

    Returns:
        list[ReportElement] | None: list of elements in the report.
    """
    db = Database()
    element_result = db.connect_execute_return(
        "SELECT id, type, data, position FROM report_elements "
        "WHERE report_id = %s ORDER BY position;",
        [report_id],
    )
    if element_result is not None:
        return list(
            map(
                lambda element: ReportElement(
                    id=element[0],
                    type=element[1],
                    data=element[2],
                    position=element[3],
                ),
                element_result,
            )
        )


def project_state(
    project_uuid: str, user: User | None, project: Project
) -> ProjectState | None:
    """Get the state variables of a project.

    Args:
        project_uuid (str): the uuid of the project to be fetched.
        user (User): the user making the request.
        project (Project): the project object with project metadata.

    Returns:
        ProjectState | None: state variables of the requested project.
    """
    with Database() as db:
        metric_results = db.execute_return(
            "SELECT id, name, type, columns FROM metrics WHERE project_uuid = %s;",
            [project_uuid],
        )
        metrics = list(
            map(
                lambda metric: Metric(
                    id=metric[0],
                    name=metric[1],
                    type=metric[2],
                    columns=metric[3],
                ),
                metric_results,
            )
        )

        slice_results = db.execute_return(
            "SELECT id, name, folder_id, filter FROM slices WHERE project_uuid = %s;",
            [
                project_uuid,
            ],
        )
        slices = list(
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

        folder_results = db.execute_return(
            "SELECT id, name, project_uuid FROM folders WHERE project_uuid = %s;",
            [
                project_uuid,
            ],
        )
        folders = list(
            map(
                lambda folder: Folder(id=folder[0], name=folder[1]),
                folder_results,
            )
        )

        tags_result = db.execute_return(
            "SELECT id, name, folder_id FROM tags WHERE project_uuid = %s",
            [
                project_uuid,
            ],
        )
        tags: list[Tag] = []
        for tag_result in tags_result:
            data_results = db.execute_return(
                sql.SQL("SELECT data_id FROM {} WHERE tag_id = %s").format(
                    sql.Identifier(f"{project_uuid}_tags_datapoints")
                ),
                [
                    tag_result[0],
                ],
            )
            tags.append(
                Tag(
                    id=tag_result[0],
                    tag_name=tag_result[1],
                    folder_id=tag_result[2],
                    data_ids=[]
                    if len(data_results) == 0
                    else [d[0] for d in data_results],
                )
            )

        column_results = db.execute_return(
            sql.SQL(
                "SELECT column_id, name, type, model, data_type FROM {} ORDER BY name;"
            ).format(sql.Identifier(f"{project_uuid}_column_map")),
        )

        columns = list(
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

        model_results = db.execute_return(
            sql.SQL("SELECT DISTINCT model FROM {} WHERE model IS NOT NULL;").format(
                sql.Identifier(f"{project_uuid}_column_map")
            ),
        )
        models = [m[0] for m in model_results]

        if user is not None:
            # Check whether the user or an org of the user have project edit rights
            user_editor = db.execute_return(
                "SELECT editor FROM user_project WHERE user_id = %s AND "
                "project_uuid = %s",
                [user.id, project_uuid],
            )
            org_editor = db.execute_return(
                "SELECT * FROM organization_project AS r JOIN user_organization "
                "AS o ON r.organization_id = o.organization_id "
                "WHERE r.project_uuid = %s AND o.user_id = %s AND r.editor = TRUE;",
                [project_uuid, user.id],
            )
            project.editor = len(org_editor) > 0 or (
                bool(user_editor[0][0]) if len(user_editor) > 0 else False
            )

        has_data = db.execute_return(
            "SELECT EXISTS (SELECT FROM information_schema.tables WHERE "
            "table_schema = 'public' AND table_name = %s);",
            [project_uuid],
        )
        if len(has_data) > 0:
            has_data = has_data[0][0]
        else:
            has_data = False

        num_likes = db.execute_return(
            "SELECT COUNT(*) FROM project_like WHERE project_uuid = %s;", [project_uuid]
        )

        user_liked = False
        if user is not None:
            user_liked = db.execute_return(
                "SELECT EXISTS(SELECT 1 FROM project_like WHERE project_uuid = %s AND "
                "user_id = %s);",
                [project_uuid, user.id],
            )
            if len(user_liked) > 0:
                user_liked = bool(user_liked[0][0])
            else:
                user_liked = False

        return ProjectState(
            project=project,
            metrics=metrics,
            folders=folders,
            columns=columns,
            slices=slices,
            tags=tags,
            models=models,
            has_data=has_data,
            num_likes=num_likes[0][0] if isinstance(num_likes[0][0], int) else 0,
            user_liked=user_liked,
        )


def project_stats(project_uuid: str, user_id: int | None = None) -> ProjectStats:
    """Get statistics for a specified project.

    Args:
        project_uuid (str): uuid of the project to get statistics for.
        user_id (int): id of the user making the request.

    Returns:
        ProjectStats | None: statistics of the specified project.
    """
    with Database() as db:
        has_data = db.execute_return(
            "SELECT EXISTS (SELECT FROM information_schema.tables WHERE "
            "table_schema = 'public' AND table_name = %s);",
            [project_uuid],
        )
        if len(has_data) > 0 and has_data[0][0]:
            num_instances = db.execute_return(
                sql.SQL("SELECT COUNT(*) FROM {};").format(sql.Identifier(project_uuid))
            )[0][0]
            num_models = db.execute_return(
                sql.SQL("SELECT COUNT(DISTINCT model) FROM {};").format(
                    sql.Identifier(f"{project_uuid}_column_map")
                )
            )[0][0]
        else:
            num_instances = 0
            num_models = 0

        num_charts = db.execute_return(
            "SELECT COUNT(*) FROM charts WHERE project_uuid = %s;", [project_uuid]
        )
        num_likes = db.execute_return(
            "SELECT COUNT(*) FROM project_like WHERE project_uuid = %s;", [project_uuid]
        )

        user_liked = False
        if user_id is not None:
            user_liked = db.execute_return(
                "SELECT EXISTS(SELECT 1 FROM project_like WHERE project_uuid = %s AND "
                "user_id = %s);",
                [project_uuid, user_id],
            )
            if len(user_liked) > 0:
                user_liked = bool(user_liked[0][0])
            else:
                user_liked = False

        return ProjectStats(
            num_instances=num_instances,
            num_models=num_models,
            num_charts=num_charts[0][0],
            num_likes=num_likes[0][0],
            user_liked=user_liked,
        )


def report_stats(report_id: int, user_id: int | None = None) -> ReportStats:
    """Get statistics for a specified report.

    Args:
        report_id (int): id of the report to get statistics for.
        user_id (int): id of the user making the request.

    Returns:
        ReportStats | None: statistics of the specified report.
    """
    with Database() as db:
        num_projects = db.execute_return(
            "SELECT COUNT(*) FROM report_project WHERE report_id = %s;",
            [report_id],
        )
        num_elements = db.execute_return(
            "SELECT COUNT(*) FROM report_elements " "WHERE report_id = %s;", [report_id]
        )
        num_likes = db.execute_return(
            "SELECT COUNT(*) FROM report_like WHERE report_id = %s;", [report_id]
        )

        user_liked = False
        if user_id is not None:
            user_liked = db.execute_return(
                "SELECT EXISTS(SELECT 1 FROM report_like WHERE report_id = %s AND "
                "user_id = %s);",
                [report_id, user_id],
            )
            if len(user_liked) > 0:
                user_liked = bool(user_liked[0][0])
            else:
                user_liked = False

        return ReportStats(
            num_projects=num_projects[0][0],
            num_elements=num_elements[0][0],
            num_likes=num_likes[0][0],
            user_liked=user_liked,
        )


def metrics(project_uuid: str) -> list[Metric]:
    """Get all metrics for a specified project.

    Args:
        project_uuid (str): the project the user is currently working with.

    Returns:
        list[Metric]: list of metrics used with the project.
    """
    db = Database()
    metric_results = db.connect_execute_return(
        "SELECT id, name, type, columns FROM metrics WHERE project_uuid = %s;",
        [project_uuid],
    )
    return list(
        map(
            lambda metric: Metric(
                id=metric[0],
                name=metric[1],
                type=metric[2],
                columns=metric[3],
            ),
            metric_results,
        )
    )


def metrics_by_id(metric_ids: list[int], project_uuid: str) -> dict[int, Metric | None]:
    """Get a list of metrics by their ids.

    Args:
        metric_ids (list[int]): list of metric ids to be fetched.
        project_uuid (str): the project the user is currently working with.

    Returns:
        list[Metric]: list of metrics as requested by the user.
    """
    db = Database()
    metric_results = db.connect_execute_return(
        "SELECT id, name, type, columns FROM metrics"
        " WHERE project_uuid = %s AND id = ANY(%s);",
        [project_uuid, [metric_ids]],
    )
    if len(metric_results) == 0:
        return {}

    ret = {}
    for m in metric_results:
        ret[m[0]] = Metric(
            id=m[0],
            name=m[1],
            type=m[2],
            columns=m[3],
        )
    return ret


def slice_by_id(slice_id: int) -> Slice:
    """Get a single slice by its ID.

    Args:
        slice_id (int): id of the slice to be fetched.

    Returns:
        Slice | None: slice as requested by the user.
    """
    db = Database()
    slice_result = db.connect_execute_return(
        "SELECT id, name, folder_id, filter, project_uuid FROM slices WHERE id = %s;",
        [slice_id],
    )

    if len(slice_result) == 0:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "ERROR: Slice could not be found."
        )

    return Slice(
        id=slice_result[0][0],
        slice_name=slice_result[0][1],
        folder_id=slice_result[0][2],
        filter_predicates=FilterPredicateGroup(
            predicates=json.loads(slice_result[0][3])["predicates"],
            join=Join.OMITTED,
        ),
        project_uuid=slice_result[0][4],
    )


def tag_by_id(tag_id: int) -> Tag:
    """Get a single tag by its ID.

    Args:
        tag_id (int): id of the tag to be fetched.

    Returns:
        Tag | None: tag as requested by the user.
    """
    with Database() as db:
        tag_result = db.connect_execute_return(
            "SELECT id, name, folder_id, project_uuid FROM tags WHERE id = %s;",
            [tag_id],
        )

        if len(tag_result) == 0:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, "ERROR: Tag could not be found."
            )
        else:
            tag_result = tag_result[0]

        data_ids = db.connect_execute_return(
            sql.SQL("SELECT data_id FROM {} WHERE tag_id = %s").format(
                sql.Identifier(f"{tag_result[3]}_tags_datapoints")
            ),
            [
                tag_result[0],
            ],
        )

        return Tag(
            id=tag_result[0],
            tag_name=tag_result[1],
            data_ids=[data_ids[0] for data_ids in data_ids],
            folder_id=tag_result[2],
            project_uuid=tag_result[3],
        )


def folders(project: str) -> list[Folder]:
    """Get a list of all folders in a project.

    Args:
        project (str): the project the user is currently working with.

    Returns:
        list[Folder]: list of folders created in the project.
    """
    db = Database()
    folder_results = db.connect_execute_return(
        "SELECT id, name, project_uuid FROM folders WHERE project_uuid = %s;",
        [
            project,
        ],
    )
    return list(
        map(
            lambda folder: Folder(id=folder[0], name=folder[1]),
            folder_results,
        )
    )


def folder(id: int) -> Folder | None:
    """Get a single folder by its ID.

    Args:
        id (int): id of the folder to be fetched.

    Returns:
        Folder | None: folder as requested by the user.
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
            id=folder_result[0][0] if isinstance(folder_result[0][0], int) else 0,
            name=str(folder_result[0][1]),
        )
        if len(folder_result) > 0
        else None
    )


def slices(project: str, ids: list[int] | None = None) -> list[Slice]:
    """Get a list of all slices of a project with certain IDs.

    Args:
        project (str): the project the user is currently working with.
        ids (list[int] | None, optional): limited list of slice IDs to fetch from,
            using all slices of the project if None. Defaults to None.

    Returns:
        list[Slice]: list of requested slices.
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
        )
    else:
        slice_results = db.connect_execute_return(
            "SELECT id, name, folder_id, filter, "
            "array_position(%s::integer[],id) as ord FROM slices "
            "WHERE project_uuid = %s AND id = ANY(%s) "
            "ORDER BY ord;",
            [
                ids,
                project,
                ids,
            ],
        )
    return list(
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


def chart(project_uuid: str, chart_id: int) -> Chart:
    """Get a project chart by its ID.

    Args:
        project_uuid (str): the project the user is currently working with.
        chart_id (int): the ID of the chart to be fetched.


    Returns:
        Chart | None: the requested chart.
    """
    db = Database()
    chart_result = db.connect_execute_return(
        "SELECT id, name, type, parameters FROM "
        "charts WHERE id = %s AND project_uuid = %s;",
        [
            chart_id,
            project_uuid,
        ],
    )
    if len(chart_result) == 0:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "ERROR: Chart could not be found."
        )
    return Chart(
        id=chart_result[0][0],
        name=chart_result[0][1],
        type=chart_result[0][2],
        project_uuid=project_uuid,
        parameters=json.loads(chart_result[0][3]),
    )


def charts(project_uuid: str) -> list[Chart]:
    """Get a list of all charts created in the project.

    Args:
        project_uuid (str): the project the user is currently working with.

    Returns:
        list[Chart]: list of all the charts in the project.
    """
    db = Database()
    chart_results = db.connect_execute_return(
        "SELECT id, name, type, parameters FROM charts WHERE project_uuid = %s"
        " ORDER BY created_at;",
        [
            project_uuid,
        ],
    )
    return list(
        map(
            lambda chart: Chart(
                id=chart[0],
                name=chart[1],
                project_uuid=project_uuid,
                type=chart[2],
                parameters=json.loads(chart[3]),
            ),
            chart_results,
        )
    )


def columns(project: str) -> list[ZenoColumn]:
    """Get a list of all columns in the project's data table.

    Args:
        project (str): the project the user is currently working with.

    Returns:
        list[ZenoColumn]: list of all the project's data columns.
    """
    db = Database()
    column_results = db.connect_execute_return(
        sql.SQL("SELECT column_id, name, type, model, data_type FROM {};").format(
            sql.Identifier(f"{project}_column_map")
        ),
    )

    return list(
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


async def histogram_buckets(
    project_uuid: str, columns: list[ZenoColumn]
) -> dict[str, list[HistogramBucket]]:
    """Get the histogram buckets for a column or create if they don't exist.

    Args:
        project_uuid (str): the project the user is currently working with.
        columns (list[ZenoColumn]): the column to get histogram buckets for.

    Returns:
        dict[str, list[HistogramBucket]]: the histogram buckets for the given columns.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                sql.SQL(
                    "SELECT column_id, histogram FROM {} WHERE "
                    + "column_id IN ({}) ORDER BY name;"
                ).format(
                    sql.Identifier(f"{project_uuid}_column_map"),
                    sql.SQL(",").join(map(sql.Literal, [c.id for c in columns])),
                )
            )

            histograms = await cur.fetchall()
            if None in [h[1] for h in histograms]:
                histograms = await asyncio.gather(
                    *[calculate_histogram_bucket(project_uuid, col) for col in columns]
                )
                histograms = {col.id: histograms[i] for i, col in enumerate(columns)}
                for col_id, hist in histograms.items():
                    await cur.execute(
                        sql.SQL(
                            "UPDATE {} SET histogram = %s WHERE column_id = %s"
                        ).format(sql.Identifier(f"{project_uuid}_column_map")),
                        (
                            json.dumps([h.model_dump(mode="json") for h in hist]),
                            col_id,
                        ),
                    )
                return histograms
            else:
                return {
                    hist[0]: [HistogramBucket.model_validate(b) for b in hist[1]]
                    for hist in histograms
                }


def table_data_paginated(
    project: str,
    filter_sql: sql.Composed | None,
    req: TableRequest,
) -> SQLTable:
    """Get a slice of the data saved in the project table.

    Args:
        project (str): the project the user is currently working with.
        filter_sql (sql.Composed | None): filter to apply before fetching a slice of
            the data.
        req (TableRequest): the request for the given table slice.

    Raises:
        Exception: something failed while reading the data from the database.

    Returns:
        SQLTable: the resulting slice of the data as requested by the user.
    """
    with Database() as db:
        if db.cur is None:
            return SQLTable(table=[], columns=[])
        filter_results = None
        columns = []

        diff_sql = sql.SQL("")
        if req.diff_column_1 is not None and req.diff_column_2 is not None:
            if req.diff_column_1.data_type == MetadataType.CONTINUOUS:
                diff_sql = sql.SQL(", {} - {} AS diff").format(
                    sql.Identifier(req.diff_column_1.id),
                    sql.Identifier(req.diff_column_2.id),
                )
            else:
                diff_sql = sql.SQL(", {} = {} AS diff").format(
                    sql.Identifier(req.diff_column_1.id),
                    sql.Identifier(req.diff_column_2.id),
                )

        filter = sql.SQL("")
        if filter_sql is not None:
            filter = sql.SQL("WHERE ") + filter_sql

        order_sql = sql.SQL("")
        if req.sort[0]:
            sort = req.sort[0].id
            if sort == "":
                sort = "diff"

            order_sql = sql.SQL("ORDER BY {} {}").format(
                sql.Identifier(sort),
                sql.SQL("DESC" if req.sort[1] else "ASC"),
            )
        else:
            id_column = db.execute_return(
                sql.SQL("SELECT column_id FROM {} WHERE type = 'ID';").format(
                    sql.Identifier(f"{project}_column_map")
                ),
            )
            if len(id_column) > 0:
                id_column = id_column[0][0]
                order_sql = sql.SQL("ORDER BY {} ASC").format(sql.Identifier(id_column))

        final_statement = sql.SQL(" ").join(
            [
                sql.SQL("SELECT *"),
                diff_sql,
                sql.SQL("FROM {}").format(sql.Identifier(project)),
                filter,
                order_sql,
                sql.SQL("LIMIT {} OFFSET {};").format(
                    sql.Literal(req.limit), sql.Literal(req.offset)
                ),
            ]
        )
        db.cur.execute(final_statement)

        if db.cur.description is not None:
            columns = [desc[0] for desc in db.cur.description]
        filter_results = db.cur.fetchall()
        return SQLTable(table=filter_results, columns=columns)


def slice_element_options(
    slice: Slice, project_uuid: str, model_name: str | None
) -> SliceElementOptions | None:
    """Get options to render slice element in reports.

    Args:
        slice (Slice): the slice to get report options for.
        project_uuid (str): the project the user is currently working with.
        model_name (str | None): the model name to get slice options for.


    Returns:
        SliceElementOptions | None: options for the slice element.
    """
    with Database() as db:
        project = db.execute_return(
            "SELECT uuid, name, view, samples_per_page, public, description, owner_id, "
            "created_at, updated_at FROM projects WHERE uuid = %s;",
            [project_uuid],
        )
        owner_name = db.execute_return(
            "SELECT name FROM users WHERE id = %s", [project[0][6]]
        )

        filter = table_filter(
            project_uuid,
            model_name,
            filter_predicates=FilterPredicateGroup(
                predicates=slice.filter_predicates.predicates,
                join=Join.OMITTED,
            ),
        )

        if filter is not None:
            slice_size = db.execute_return(
                sql.SQL("SELECT COUNT(*) FROM {} WHERE ").format(
                    sql.Identifier(project_uuid)
                )
                + filter
            )
        else:
            slice_size = [[0]]

        column_names = db.execute_return(
            sql.SQL(
                "SELECT column_id, type FROM {} WHERE model = %s OR model IS NULL;"
            ).format(sql.Identifier(f"{project_uuid}_column_map")),
            [model_name],
        )
        id_column = ""
        data_column = None
        label_column = None
        model_column = None
        for col_id, col_type in column_names:
            if col_type == ZenoColumnType.ID:
                id_column = col_id
            elif col_type == ZenoColumnType.DATA:
                data_column = col_id
            elif col_type == ZenoColumnType.LABEL:
                label_column = col_id
            elif col_type == ZenoColumnType.OUTPUT:
                model_column = col_id

        return SliceElementOptions(
            slice_name=slice.slice_name,
            slice_size=slice_size[0][0] if len(slice_size) > 0 else 0,
            id_column=id_column,
            data_column=data_column,
            label_column=label_column,
            model_column=model_column,
            project=Project(
                uuid=project[0][0],
                name=project[0][1],
                description=project[0][5],
                owner_name=owner_name[0][0],
                view=match_instance_view(project[0][2]),
                editor=False,
                created_at=project[0][7].isoformat(),
                updated_at=project[0][8].isoformat(),
            ),
        )


def tag_element_options(
    tag: Tag, project_uuid: str, model_name: str | None
) -> TagElementOptions:
    """Get options to render tag element in reports.

    Args:
        tag (Tag): the tag to get report options for.
        project_uuid (str): the project the user is currently working with.
        model_name (str | None): the model name to get tag options for.

    Returns:
        TagElementOptions | None: options for the tag element.
    """
    with Database() as db:
        tag_ids = db.execute_return(
            sql.SQL("SELECT data_id FROM {} WHERE tag_id = %s").format(
                sql.Identifier(f"{project_uuid}_tags_datapoints")
            ),
            [
                tag.id,
            ],
        )

        project = db.execute_return(
            "SELECT uuid, name, view, samples_per_page, public, description, owner_id, "
            "created_at, updated_at FROM projects WHERE uuid = %s;",
            [project_uuid],
        )
        if len(project) == 0:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "ERROR: Could not find corresponding project.",
            )

        owner_name = db.execute_return(
            "SELECT name FROM users WHERE id = %s", [project[0][6]]
        )

        filter = table_filter(
            project_uuid,
            model_name,
            data_ids=[tag_id[0] for tag_id in tag_ids],
        )

        if filter is not None:
            tag_size = db.execute_return(
                sql.SQL("SELECT COUNT(*) FROM {} WHERE ").format(
                    sql.Identifier(project_uuid)
                )
                + filter
            )
        else:
            tag_size = [[0]]

        column_names = db.execute_return(
            sql.SQL(
                "SELECT column_id, type FROM {} WHERE model = %s OR model IS NULL;"
            ).format(sql.Identifier(f"{project_uuid}_column_map")),
            [model_name],
        )
        id_column = ""
        data_column = None
        label_column = None
        model_column = None
        for col_id, col_type in column_names:
            if col_type == ZenoColumnType.ID:
                id_column = col_id
            elif col_type == ZenoColumnType.DATA:
                data_column = col_id
            elif col_type == ZenoColumnType.LABEL:
                label_column = col_id
            elif col_type == ZenoColumnType.OUTPUT:
                model_column = col_id

        return TagElementOptions(
            tag_name=tag.tag_name,
            tag_size=tag_size[0][0] if len(tag_size) > 0 else 0,
            id_column=id_column,
            data_column=data_column,
            label_column=label_column,
            model_column=model_column,
            project=Project(
                uuid=project[0][0],
                name=project[0][1],
                description=project[0][5],
                owner_name=owner_name[0][0],
                view=match_instance_view(project[0][2]),
                editor=False,
                created_at=project[0][7].isoformat(),
                updated_at=project[0][8].isoformat(),
            ),
        )


def slice_or_tag_table(
    project_uuid: str,
    filter_sql: sql.Composed | None,
    req: SliceTableRequest | TagTableRequest,
) -> SQLTable:
    """Get a slice of the data saved in the project table.

    Args:
        project_uuid (str): uuid of the project to the user is currently working with.
        filter_sql (sql.Composed | None): filter to apply before fetching a slice of
            the data.
        req (SliceTableRequest | TagTableRequest): request for the given table slice.

    Raises:
        Exception: something failed while reading the data from the database.

    Returns:
        SQLTable: the resulting slice of the data as requested by the user.
    """
    with Database() as db:
        if db.cur is None:
            return SQLTable(table=[], columns=[])
        filter_results = None
        columns = []

        filter = sql.SQL("")
        if filter_sql is not None:
            filter = sql.SQL("WHERE ") + filter_sql

        final_statement = sql.SQL(" ").join(
            [
                sql.SQL("SELECT *"),
                sql.SQL("FROM {}").format(sql.Identifier(project_uuid)),
                filter,
                sql.SQL("LIMIT {} OFFSET {};").format(
                    sql.Literal(req.limit), sql.Literal(req.offset)
                ),
            ]
        )
        db.cur.execute(final_statement)

        if db.cur.description is not None:
            columns = [desc[0] for desc in db.cur.description]
        filter_results = db.cur.fetchall()
        return SQLTable(table=filter_results, columns=columns)


def slice_instance_ids(
    project_uuid: str, filter_sql: sql.Composed | None, id_column: ZenoColumn
) -> list[str]:
    """Get all data ids for a slice.

    Args:
        project_uuid (str): project the slice belongs to.
        filter_sql (sql.Composed | None): filter specified by the slice.
        id_column (ZenoColumn): identifier of the instance id column in the project.

    Returns:
        list[str]: list of instance ids that belong to the slice.
    """
    with Database() as db:
        filter = sql.SQL("")
        if filter_sql is not None:
            filter = sql.SQL("WHERE ") + filter_sql

        final_statement = sql.SQL(" ").join(
            [
                sql.SQL("SELECT {} FROM {}").format(
                    sql.Identifier(id_column.id), sql.Identifier(project_uuid)
                ),
                filter,
            ]
        )
        results = db.execute_return(final_statement)
        return list(map(lambda res: str(res[0]), results))


def table_data(project: str, filter_sql: sql.Composed | None) -> SQLTable:
    """Get the filtered data table for the current project.

    Args:
        project (str): the project the user is currently working with.
        filter_sql (sql.Composed | None): filters to apply to the fetched data.

    Raises:
        Exception: something failed while reading the data from the database.

    Returns:
        SQLTable: the filtered data table for the project.
    """
    with Database() as db:
        filter_results = None
        columns = []
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


def column(
    project: str, column: ZenoColumn, filter_sql: sql.Composed | None = None
) -> list[str | int | float | bool]:
    """Get the data for one column of the project's data table.

    Args:
        project (str): the project the user is currently working with.
        column (ZenoColumn): the column for which to fetch the data.
        filter_sql (sql.Composed | None, optional): any filters to apply before
            fetching the column data. Defaults to None.

    Returns:
        list[str | int | float | bool]: the data that is stored in the requested
            column.
    """
    db = Database()
    if filter_sql is None:
        column_result = db.connect_execute_return(
            sql.SQL("SELECT {} FROM {}").format(
                sql.Identifier(column.id), sql.Identifier(project)
            ),
        )
    else:
        column_result = db.connect_execute_return(
            sql.SQL("SELECT {} FROM {} WHERE ").format(
                sql.Identifier(column.id), sql.Identifier(project)
            )
            + filter_sql,
        )
    return list(map(lambda column: column[0], column_result))


def tags(project: str) -> list[Tag]:
    """Get a list of all tags created for a project.

    Args:
        project (str): the project the user is currently working with.

    Raises:
        Exception: something went wrong while extracting the tags from the database.

    Returns:
        list[Tag]: the list of tags associated with a project.
    """
    with Database() as db:
        tags_result = db.execute_return(
            "SELECT id, name, folder_id FROM tags WHERE project_uuid = %s",
            [
                project,
            ],
        )
        if len(tags_result) == 0:
            return []
        tags: list[Tag] = []
        for tag_result in tags_result:
            data_results = db.execute_return(
                sql.SQL("SELECT data_id FROM {} WHERE tag_id = %s").format(
                    sql.Identifier(f"{project}_tags_datapoints")
                ),
                [
                    tag_result[0],
                ],
            )
            tags.append(
                Tag(
                    id=tag_result[0],
                    tag_name=tag_result[1],
                    folder_id=tag_result[2],
                    data_ids=[]
                    if len(data_results) == 0
                    else [d[0] for d in data_results],
                )
            )
        return tags


def user(name: str) -> User | None:
    """Get the user with a specific name.

    Args:
        name (str): the name of the user for which to fetch the user.

    Returns:
        User | None: the requested user.
    """
    db = Database()
    user = db.connect_execute_return(
        "SELECT id, name, cognito_id FROM users WHERE name = %s", [name]
    )
    if len(user) == 0:
        return None
    user = user[0]
    return User(
        id=user[0] if isinstance(user[0], int) else -1,
        name=str(user[1]),
        cognito_id=user[2],
        admin=None,
    )


def users() -> list[User]:
    """Get a list of all registered users.

    Returns:
        list[User]: all registered users.
    """
    db = Database()
    users = db.connect_execute_return("SELECT id, name, cognito_id FROM users;")
    return list(
        map(
            lambda user: User(id=user[0], name=user[1], cognito_id=user[2], admin=None),
            users,
        )
    )


def organizations() -> list[Organization]:
    """Get a list of all organizations.

    Returns:
        list[Organization]: all organizations in the database.
    """
    db = Database()
    organizations = db.connect_execute_return("SELECT id, name FROM organizations;")
    return list(
        map(
            lambda organization: Organization(
                id=organization[0], name=organization[1], admin=False, members=[]
            ),
            organizations,
        )
    )


def user_organizations(user: User) -> list[Organization]:
    """Get the organizations that a user is a member of.

    Args:
        user (User): the user for which to fetch available organizations.

    Returns:
        list[Organization]: all organizations the user is a member of.
    """
    organizations: list[Organization] = []
    with Database() as db:
        organizations_result = db.execute_return(
            "SELECT o.id, o.name, uo.admin FROM organizations AS o "
            "JOIN user_organization AS uo ON o.id = uo.organization_id "
            "WHERE uo.user_id = %s;",
            [user.id],
        )
        if len(organizations_result) == 0:
            return organizations
        for org in organizations_result:
            members = db.execute_return(
                "SELECT u.id, u.name, uo.admin FROM users as u "
                "JOIN user_organization as uo ON u.id = uo.user_id "
                "WHERE uo.organization_id = %s;",
                [org[0]],
            )
            organizations.append(
                Organization(
                    id=org[0],
                    name=org[1],
                    admin=org[2],
                    members=list(
                        map(
                            lambda member: User(
                                id=member[0],
                                name=member[1],
                                admin=member[2],
                            ),
                            members,
                        )
                    ),
                )
            )
        return organizations


def project_users(project: str) -> list[User]:
    """Get all the users that have access to a project.

    Args:
        project (str): the project for which to get user access.

    Returns:
        list[User]: the list of users who can access the project.
    """
    db = Database()
    project_users = db.connect_execute_return(
        "SELECT u.id, u.name, up.editor FROM users as u "
        "JOIN user_project AS up ON u.id = up.user_id WHERE up.project_uuid = %s",
        [project],
    )
    return list(
        map(
            lambda user: User(id=user[0], name=user[1], admin=user[2]),
            project_users,
        )
    )


def report_users(report_id: int) -> list[User]:
    """Get all the users that have access to a report.

    Args:
        report_id (int): the report for which to get user access.

    Returns:
        list[User]: the list of users who can access the report.
    """
    db = Database()
    report_users = db.connect_execute_return(
        "SELECT u.id, u.name, ur.editor FROM users as u "
        "JOIN user_report AS ur ON u.id = ur.user_id WHERE ur.report_id = %s",
        [report_id],
    )
    return list(
        map(
            lambda user: User(id=user[0], name=user[1], admin=user[2]),
            report_users,
        )
    )


def project_orgs(project: str) -> list[Organization]:
    """Get all the organizations that have access to a project.

    Args:
        project (str): the project for which to get organization access.

    Returns:
        list[Organization]: the list of organizations who can access the project.
    """
    db = Database()
    project_organizations = db.connect_execute_return(
        "SELECT o.id, o.name, op.editor FROM organizations as o "
        "JOIN organization_project AS op ON o.id = op.organization_id "
        "WHERE op.project_uuid = %s",
        [project],
    )
    return list(
        map(
            lambda org: Organization(id=org[0], name=org[1], members=[], admin=org[2]),
            project_organizations,
        )
    )


def report_orgs(report_id: int) -> list[Organization]:
    """Get all the organizations that have access to a report.

    Args:
        report_id (int): the report for which to get organization access.

    Returns:
        list[Organization]: the list of organizations who can access the report.
    """
    db = Database()
    report_organizations = db.connect_execute_return(
        "SELECT o.id, o.name, orep.editor FROM organizations as o "
        "JOIN organization_report AS orep ON o.id = orep.organization_id "
        "WHERE orep.report_id = %s",
        [report_id],
    )
    return list(
        map(
            lambda org: Organization(id=org[0], name=org[1], members=[], admin=org[2]),
            report_organizations,
        )
    )


def filtered_short_string_column_values(
    project: str, req: StringFilterRequest
) -> list[str]:
    """Select distinct string values of a column and return their short representation.

    Args:
        project (str): the project for which to filter the column
        req (StringFilterRequest): the specification of the filter operation.

    Returns:
        list[str]: the filtered string column data.
    """
    db = Database()

    if req.operation == Operation.LIKE or req.operation == Operation.ILIKE:
        req.filter_string = "%" + req.filter_string + "%"

    returned_strings = db.connect_execute_return(
        sql.SQL("SELECT {} from {} WHERE {} {} %s;").format(
            sql.Identifier(req.column.id),
            sql.Identifier(project),
            sql.Identifier(req.column.id),
            sql.SQL(req.operation.literal()),
        ),
        [
            req.filter_string,
        ],
    )

    short_ret: list[str] = []
    if len(returned_strings) == 0:
        return short_ret
    for result in returned_strings[0:5]:
        idx = result[0].find(req.filter_string)
        loc_str = result[0][0 if idx < 20 else idx - 20 : idx + 20]
        if len(result[0]) > 40 + len(req.filter_string):
            if idx - 20 > 0:
                loc_str = "..." + loc_str
            if idx + 20 < len(result[0]):
                loc_str = loc_str + "..."
        short_ret.append(loc_str)

    return short_ret


def system_exists(project_uuid: str, system_name: str) -> bool:
    """Check whether a system exists for a project.

    Args:
        project_uuid (str): ID of the project.
        system_name (str): name of the system.

    Returns:
        bool: whether the system exists.

    Raises:
        Exception: something went wrong while checking whether the system exists.
    """
    db = Database()
    exists = db.connect_execute_return(
        sql.SQL("SELECT EXISTS(SELECT 1 FROM {} " "WHERE model = %s);").format(
            sql.Identifier(f"{project_uuid}_column_map")
        ),
        [system_name],
    )
    if len(exists) > 0:
        return bool(exists[0][0])
    else:
        raise Exception("Error while checking whether system exists.")
