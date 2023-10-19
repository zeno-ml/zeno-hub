"""Functions to insert new data into Zeno's database."""
import json
import secrets
import uuid

from pgpq import ArrowToPostgresBinaryEncoder
from psycopg import sql
from pyarrow import RecordBatch, Schema

import zeno_backend.database.delete as delete
from zeno_backend.classes.base import MetadataType, ZenoColumn, ZenoColumnType
from zeno_backend.classes.chart import Chart, ParametersEncoder
from zeno_backend.classes.filter import (
    FilterPredicate,
    FilterPredicateGroup,
    Join,
    Operation,
    PredicatesEncoder,
)
from zeno_backend.classes.project import Project
from zeno_backend.classes.report import ReportElement
from zeno_backend.classes.slice import Slice
from zeno_backend.classes.tag import Tag
from zeno_backend.classes.user import Organization, User
from zeno_backend.database.database import Database, db_pool
from zeno_backend.database.util import hash_api_key, resolve_metadata_type


def api_key(user: User) -> str | None:
    """Generate an API key for the user and save the hash.

    Args:
        user (User): the user for which to fetch the API key.

    Returns:
        str | None: the API key of the user.
    """
    # Generate a new API key for the user.
    api_key = "zen_" + secrets.token_urlsafe(32)
    hashed_api_key = hash_api_key(api_key)

    # Set the API key hash in the database.
    db = Database()
    db.connect_execute(
        "UPDATE users SET api_key_hash = %s WHERE id = %s;",
        [hashed_api_key, user.id],
    )

    return api_key


def project(project_config: Project, owner_id: int):
    """Setting up a new project in Zeno.

    Creates a new entry in the projects table, creates a new table for the project's
    data, creates a table to map data columns to ids and types, and creates a table for
    all tags of the project.

    Args:
        project_config (Project): the configuration with which to
            initialize the new project.
        owner_id (int): the id of the user who owns the project.

    Raises:
        Exception: something went wrong in the process of creating the new project in
            the database.
    """
    with Database() as db:
        db.execute(
            "INSERT INTO projects (uuid, name, owner_id, view, "
            + "samples_per_page, public, description) "
            + "VALUES (%s,%s,%s,%s,%s,%s,%s);",
            [
                project_config.uuid,
                project_config.name,
                owner_id,
                project_config.view,
                project_config.samples_per_page,
                project_config.public,
                project_config.description,
            ],
        )
        db.execute(
            "INSERT INTO user_project (user_id, project_uuid, editor) "
            "VALUES (%s,%s,%s)",
            [owner_id, project_config.uuid, True],
        )
        # Create table to hold information about the columns in the project data.
        db.execute(
            sql.SQL(
                "CREATE TABLE {}(column_id TEXT NOT NULL PRIMARY KEY, "
                "name TEXT NOT NULL, type TEXT NOT NULL, model TEXT, "
                "data_type TEXT NOT NULL, histogram JSONB);"
            ).format(sql.Identifier(f"{project_config.uuid}_column_map"))
        )

        # Add metrics to the metrics table.
        for metric in project_config.metrics:
            db.execute(
                "INSERT INTO metrics (project_uuid, name, type, columns) VALUES "
                "(%s, %s, %s, %s);",
                [project_config.uuid, metric.name, metric.type, metric.columns],
            )

        db.commit()


async def dataset_schema(
    project_uuid: str,
    id_column: str,
    data_column: str,
    label_column: str,
    pa_schema: Schema,
) -> list[str]:
    """Adding a dataset schema column_map to an existing project.

    Args:
        project_uuid (str): the project the user is currently working with.
        id_column (str): the column of the dataset that contains the ids.
        data_column (str): the column of the dataset that contains the data.
        label_column (str): the column of the dataset that contains the labels.
        pa_schema (Schema): the PyArrow schema of the dataset to be added.

    Returns:
        list[str]: the ids of the columns in the dataset schema.
    """
    await delete.dataset(project_uuid)

    columns: list[ZenoColumn] = []
    for col in pa_schema:
        id_uuid = str(uuid.uuid4())
        column_type = ZenoColumnType.FEATURE
        if col.name == id_column:
            column_type = ZenoColumnType.ID
            id_column = id_uuid
        elif col.name == label_column:
            column_type = ZenoColumnType.LABEL
        elif col.name == data_column:
            column_type = ZenoColumnType.DATA

        columns.append(
            ZenoColumn(
                id=id_uuid,
                name=col.name,
                column_type=column_type,
                data_type=resolve_metadata_type(col.type),
            )
        )

    encoder = ArrowToPostgresBinaryEncoder(pa_schema)
    pg_schema = encoder.schema()
    cols = sql.SQL(",").join(
        [
            sql.Identifier(columns[i].id)
            + sql.SQL(" ")
            + sql.SQL(col[1].data_type.ddl())
            for i, col in enumerate(pg_schema.columns)
        ]
    )

    # Create and populate column_map table.
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            for column in columns:
                await cur.execute(
                    sql.SQL(
                        "INSERT INTO {} (column_id, name, type, data_type) "
                        "VALUES (%s,%s,%s,%s);"
                    ).format(sql.Identifier(f"{project_uuid}_column_map")),
                    [column.id, column.name, column.column_type, column.data_type],
                )

            await cur.execute(
                sql.SQL("CREATE TABLE IF NOT EXISTS {} (").format(
                    sql.Identifier(project_uuid)
                )
                + cols
                + sql.SQL(")")
            )

            # Make ID column primary key.
            await cur.execute(
                sql.SQL("ALTER TABLE {} ADD PRIMARY KEY ({});").format(
                    sql.Identifier(project_uuid),
                    sql.Identifier(id_column),
                )
            )

            # Create table to hold information about tags and associated datapoints.
            await cur.execute(
                sql.SQL(
                    "CREATE TABLE {}(id integer GENERATED ALWAYS AS IDENTITY PRIMARY "
                    "KEY, tag_id integer NOT "
                    "NULL REFERENCES tags(id) ON DELETE CASCADE "
                    "ON UPDATE CASCADE, data_id text NOT NULL REFERENCES {}({}) "
                    "ON DELETE CASCADE ON UPDATE CASCADE);"
                ).format(
                    sql.Identifier(f"{project_uuid}_tags_datapoints"),
                    sql.Identifier(project_uuid),
                    sql.Identifier(id_column),
                )
            )

    return [c.id for c in columns]


async def dataset(project_uuid: str, batch: RecordBatch):
    """Adds a dataset to an existing project.

    Args:
        project_uuid (str): project the user is currently working with.
        batch (RecordBatch): dataset to be added.
    """
    encoder = ArrowToPostgresBinaryEncoder(batch.schema)
    pg_schema = encoder.schema()
    cols = sql.SQL(",").join(
        [
            sql.Identifier(col_name) + sql.SQL(" ") + sql.SQL(col.data_type.ddl())
            for col_name, col in pg_schema.columns
        ]
    )

    async with db_pool.connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("DROP TABLE IF EXISTS temp_data")
            await cursor.execute(
                sql.SQL("CREATE TABLE temp_data (") + cols + sql.SQL(")")
            )
            async with cursor.copy(
                "COPY temp_data FROM STDIN WITH (FORMAT BINARY)"
            ) as copy:
                await copy.write(encoder.write_header())
                await copy.write(encoder.write_batch(batch))
                await copy.write(encoder.finish())
            await cursor.execute(
                sql.SQL("INSERT INTO {} SELECT * FROM temp_data").format(
                    sql.Identifier(project_uuid)
                )
            )
        await conn.commit()


async def system_schema(
    project_uuid: str,
    system_name: str,
    id_column: str,
    output_column: str,
    pa_schema: Schema,
) -> list[str]:
    """Adding a system schema column_map to an existing project.

    Args:
        project_uuid (str): the project the user is currently working with.
        system_name (str): the name of the system.
        id_column (str): the column of the system output that contains the ids.
        output_column (str): the column of the system output that contains the output.
        pa_schema (Schema): the PyArrow schema of the system output to be added.
    """
    await delete.system(project_uuid, system_name)

    # add columns to column_map
    columns: list[ZenoColumn] = []
    for col in pa_schema:
        if col.name == id_column:
            # get id column id
            db = Database()
            id_col = db.connect_execute_return(
                sql.SQL("SELECT column_id FROM {} WHERE type = 'ID';").format(
                    sql.Identifier(f"{project_uuid}_column_map")
                )
            )
            if id_col is None or len(id_col) == 0:
                raise Exception("ERROR: No ID column found.")

            columns.append(
                ZenoColumn(
                    id=id_col[0][0],
                    name="",
                    column_type=ZenoColumnType.ID,
                    data_type=MetadataType.OTHER,
                    model=system_name,
                )
            )
            continue
        elif col.name == output_column:
            column_type = ZenoColumnType.OUTPUT
        else:
            column_type = ZenoColumnType.FEATURE

        columns.append(
            ZenoColumn(
                id=str(uuid.uuid4()),
                name=col.name,
                column_type=column_type,
                data_type=resolve_metadata_type(col.type),
                model=system_name,
            )
        )

    encoder = ArrowToPostgresBinaryEncoder(pa_schema)
    pg_schema = encoder.schema()

    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            for i, column in enumerate(columns):
                if column.column_type == ZenoColumnType.ID:
                    continue
                await cur.execute(
                    sql.SQL(
                        "INSERT INTO {} (column_id, name, type, data_type, model) "
                        "VALUES (%s,%s,%s,%s,%s);"
                    ).format(sql.Identifier(f"{project_uuid}_column_map")),
                    [
                        column.id,
                        column.name,
                        column.column_type,
                        column.data_type,
                        column.model,
                    ],
                )
                await cur.execute(
                    sql.SQL("ALTER TABLE {} ADD COLUMN IF NOT EXISTS {} ").format(
                        sql.Identifier(project_uuid),
                        sql.Identifier(column.id),
                    )
                    + sql.SQL(pg_schema.columns[i][1].data_type.ddl())
                )
                await conn.commit()

    return [c.id for c in columns]


async def system(
    project_uuid: str,
    batch: RecordBatch,
):
    """Adds a system to an existing project.

    Args:
        project_uuid (str): project the user is currently working with.
        system_name (str): name of the system that produced the output.
        batch (RecordBatch): system output to be added.
    """
    encoder = ArrowToPostgresBinaryEncoder(batch.schema)
    pg_schema = encoder.schema()
    cols = sql.SQL(",").join(
        [
            sql.Identifier(col_name) + sql.SQL(" ") + sql.SQL(col.data_type.ddl())
            for col_name, col in pg_schema.columns
        ]
    )

    async with db_pool.connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("DROP TABLE IF EXISTS temp_data")
            await cursor.execute(
                sql.SQL("CREATE TABLE temp_data (") + cols + sql.SQL(")")
            )
            async with cursor.copy(
                "COPY temp_data FROM STDIN WITH (FORMAT BINARY)"
            ) as copy:
                await copy.write(encoder.write_header())
                await copy.write(encoder.write_batch(batch))
                await copy.write(encoder.finish())

            await cursor.execute(
                sql.SQL("SELECT column_id FROM {} WHERE type = 'ID';").format(
                    sql.Identifier(f"{project_uuid}_column_map")
                )
            )
            col_id = await cursor.fetchone()
            if col_id is None:
                raise Exception("ERROR: No ID column found.")
            col_id = col_id[0]

            await cursor.execute(
                sql.SQL("UPDATE {} AS e SET ").format(sql.Identifier(project_uuid))
                + sql.SQL(",").join(
                    [
                        sql.SQL("{} = COALESCE({}, {})").format(
                            sql.Identifier(col_name),
                            sql.Identifier("t", col_name),
                            sql.Identifier("e", col_name),
                        )
                        for col_name, _ in pg_schema.columns
                    ]
                )
                + sql.SQL(" FROM temp_data AS t WHERE {} = {}").format(
                    sql.Identifier("t", col_id),
                    sql.Identifier("e", col_id),
                )
            )
        await conn.commit()


def report(name: str, user: User):
    """Adding a report to Zeno.

    Args:
        name (str): how the report is called.
        user (User): user who created the report.
    """
    db = Database()
    db.connect_execute(
        "INSERT INTO reports (name, owner_id, public) VALUES (%s,%s,%s);",
        [name, user.id, False],
    )


def report_element(report_id: int, element: ReportElement) -> int | None:
    """Adding a report element to a Zeno Report.

    Args:
        report_id (int): the id of the report the element is added to.
        element (ReportElement): the element to be added to the report.


    Returns:
        int | None: the id of the newly created report element.
    """
    db = Database()
    id = db.connect_execute_return(
        "INSERT INTO report_elements (report_id, type, data, position)"
        " VALUES (%s,%s,%s,%s) RETURNING id;",
        [report_id, element.type, element.data, element.position],
    )
    # update position of all elements after insert
    db.connect_execute(
        "UPDATE report_elements SET position = position + 1 WHERE report_id = %s "
        "AND position >= %s;",
        [report_id, element.position],
    )
    if len(id) > 0:
        return id[0][0]


def like_report(user_id: int, report_id: int):
    """Like a report.

    Args:
        user_id: the id of the user liking the report.
        report_id: the id of the report to be liked.
    """
    with Database() as db:
        user_liked = db.execute_return(
            "SELECT id FROM report_like WHERE user_id = %s AND report_id = %s;",
            [user_id, report_id],
        )
        if len(user_liked) > 0:
            # remove like
            db.execute(
                "DELETE FROM report_like WHERE user_id = %s AND report_id = %s;",
                [user_id, report_id],
            )
            db.commit()
        else:
            db.connect_execute(
                "INSERT INTO report_like (user_id, report_id) VALUES (%s,%s);",
                [user_id, report_id],
            )


def like_project(user_id: int, project_uuid: str):
    """Like a report.

    Args:
        user_id: the id of the user liking the report.
        project_uuid: the uuid of the project to be liked.
    """
    with Database() as db:
        user_liked = db.execute_return(
            "SELECT id FROM project_like WHERE user_id = %s AND project_uuid = %s;",
            [user_id, project_uuid],
        )
        if len(user_liked) > 0:
            # remove like
            db.execute(
                "DELETE FROM project_like WHERE user_id = %s AND project_uuid = %s;",
                [user_id, project_uuid],
            )
            db.commit()
        else:
            db.connect_execute(
                "INSERT INTO project_like (user_id, project_uuid) VALUES (%s,%s);",
                [user_id, project_uuid],
            )


def folder(project: str, name: str) -> int | None:
    """Adding a folder to an existing project.

    Args:
        project (str): the project the user is currently working with.
        name (str): name of the folder to be added.


    Returns:
        int | None: the id of the newly created folder.
    """
    db = Database()
    id = db.connect_execute_return(
        "INSERT INTO folders (name, project_uuid) VALUES (%s,%s) RETURNING id;",
        [name, project],
    )
    if id is not None and len(id) > 0:
        return id[0][0]


def slice(project: str, req: Slice) -> int | None:
    """Add a slice to an existing project.

    Args:
        project (str): the project the user is currently working with.
        req (Slice): the slice to be added to the project.

    Returns:
        int | None: the id of the newly created slice.
    """
    db = Database()
    ids = db.connect_execute_return(
        "INSERT INTO slices (name, folder_id, filter, project_uuid) "
        "VALUES (%s,%s,%s,%s) RETURNING id;",
        [
            req.slice_name,
            req.folder_id,
            json.dumps(req.filter_predicates, cls=PredicatesEncoder),
            project,
        ],
    )
    if ids is not None:
        return ids[0][0]
    else:
        return None


async def all_slices_for_column(
    project: str, column: ZenoColumn, name: str | None = None
) -> list[int] | None:
    """Add slices for all values of a nominal data column.

    Args:
        project (str): project to add the slices to.
        column (ZenoColumn): column for which to add slices.
        name (str | None): name of the folder to add the slices to.

    Returns:
        list[int]|None: ids of all added slices.
    """
    ids = []
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                sql.SQL("SELECT DISTINCT {} FROM {}").format(
                    sql.Identifier(column.id), sql.Identifier(project)
                )
            )
            values = await cur.fetchall()
            if len(values) > 100:
                raise Exception("Too many distinct values to create slices for.")
            folder_id = None
            if len(values) > 0:
                await cur.execute(
                    "INSERT INTO folders (name, project_uuid) VALUES (%s,%s) "
                    "RETURNING id;",
                    [name if name is not None else column.name, project],
                )
                folder_id = await cur.fetchone()
            for value in values:
                slice = Slice(
                    id=-1,
                    slice_name=str(value[0]),
                    filter_predicates=FilterPredicateGroup(
                        predicates=[
                            FilterPredicate(
                                column=column,
                                operation=Operation.EQUAL,
                                value=value[0],
                                join=Join.OMITTED,
                            )
                        ],
                        join=Join.OMITTED,
                    ),
                    folder_id=None if folder_id is None else folder_id[0],
                )
                await cur.execute(
                    sql.SQL(
                        "SELECT id FROM slices WHERE name={} AND project_uuid={};"
                    ).format(slice.slice_name, project)
                )
                exists = await cur.fetchall()
                if len(exists) == 0:
                    await cur.execute(
                        "INSERT INTO slices (name, filter, project_uuid, folder_id) "
                        "VALUES (%s,%s,%s,%s) RETURNING id;",
                        [
                            slice.slice_name,
                            json.dumps(slice.filter_predicates, cls=PredicatesEncoder),
                            project,
                            slice.folder_id,
                        ],
                    )
                    id = await cur.fetchone()
                    if id is not None:
                        ids.append(id[0])
    return ids


def chart(project: str, chart: Chart) -> int | None:
    """Add a chart to an existing project.

    Args:
        project (str): the project the user is currently working with.
        chart (Chart): the chart to be added to the project.


    Returns:
        int | None: the id of the newly created chart.
    """
    db = Database()
    id = db.connect_execute_return(
        "INSERT INTO charts (name, type, parameters, project_uuid) "
        "VALUES (%s,%s,%s,%s) RETURNING id;",
        [
            chart.name,
            chart.type,
            json.dumps(chart.parameters, cls=ParametersEncoder),
            project,
        ],
    )
    if id is not None and len(id) > 0:
        return id[0][0]


def tag(project: str, tag: Tag) -> int | None:
    """Add a tag to an existing project.

    Args:
        project (str): the project the user is currently working with.
        tag (Tag): the tag to be added to the project.

    Returns:
        int | None: the id of the newly created tag.
    """
    with Database() as db:
        id = db.execute_return(
            "INSERT INTO tags (name, folder_id, project_uuid) VALUES (%s,%s,%s) "
            "RETURNING id;",
            [tag.tag_name, tag.folder_id, project],
        )
        if id is None or len(id) == 0:
            return
        for datapoint in tag.data_ids:
            db.execute(
                sql.SQL("INSERT INTO {} (tag_id, data_id) VALUES (%s,%s);").format(
                    sql.Identifier(f"{project}_tags_datapoints")
                ),
                [id[0][0], datapoint],
            )
        db.commit()
        return id[0][0]


def user(user: User) -> int | None:
    """Add a new user to the database.

    Args:
        user (User): the user to be added.
    """
    db = Database()
    id = db.connect_execute_return(
        'INSERT INTO users ("name", cognito_id) values(%s, %s) RETURNING id;',
        [user.name, user.cognito_id],
    )
    if id is not None:
        return id[0][0]


def organization(user: User, organization: Organization):
    """Add a new organization to the database.

    Args:
        user (User): the user who created the organization.
        organization (Organization): the organization to be created.
    """
    with Database() as db:
        id = db.execute_return(
            "INSERT INTO organizations (name) VALUES (%s) RETURNING id;",
            [organization.name],
        )
        if id is None:
            return
        db.execute(
            "INSERT INTO user_organization (user_id, organization_id, admin) "
            "VALUES (%s,%s,%s);",
            [user.id, id[0][0], True],
        )
        db.commit()


def project_user(project: str, user: User):
    """Add a user to a project.

    Args:
        project (str): the project id to add the user to.
        user (User): the user to add to the project.
    """
    db = Database()
    db.connect_execute(
        "INSERT INTO user_project (user_id, project_uuid, editor) VALUES (%s,%s,%s)",
        [user.id, project, user.admin],
    )


def project_org(project: str, organization: Organization):
    """Add a organization to a project.

    Args:
        project (str): the project id to add the organization to.
        organization (Organization): the organization to add to the project.
    """
    db = Database()
    db.connect_execute(
        "INSERT INTO organization_project (organization_id, project_uuid, editor) "
        "VALUES (%s,%s,%s)",
        [organization.id, project, organization.admin],
    )


def report_user(report_id: int, user: User):
    """Add a user to a report.

    Args:
        report_id (int): the report id to add the user to.
        user (User): the user to add to the report.
    """
    db = Database()
    db.connect_execute(
        "INSERT INTO user_report (user_id, report_id, editor) VALUES (%s,%s,%s)",
        [user.id, report_id, user.admin],
    )


def report_org(report_id: int, organization: Organization):
    """Add a organization to a report.

    Args:
        report_id (int): the report id to add the organization to.
        organization (Organization): the organization to add to the report.
    """
    db = Database()
    db.connect_execute(
        "INSERT INTO organization_report (organization_id, report_id, editor) "
        "VALUES (%s,%s,%s)",
        [organization.id, report_id, organization.admin],
    )
