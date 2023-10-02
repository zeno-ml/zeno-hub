"""Functions to insert new data into Zeno's database."""
import json
import secrets
import uuid

import pandas as pd
from pgpq import ArrowToPostgresBinaryEncoder
from psycopg import sql
from pyarrow import RecordBatch
from sqlalchemy import create_engine

from zeno_backend.classes.base import MetadataType, ZenoColumn, ZenoColumnType
from zeno_backend.classes.chart import Chart, ParametersEncoder
from zeno_backend.classes.filter import PredicatesEncoder
from zeno_backend.classes.project import Project
from zeno_backend.classes.report import ReportElement
from zeno_backend.classes.sdk import DatasetSchema
from zeno_backend.classes.slice import Slice
from zeno_backend.classes.tag import Tag
from zeno_backend.classes.user import Organization, User
from zeno_backend.database.database import Database, db_pool
from zeno_backend.database.database import config as config_db
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
            "INSERT INTO projects (uuid, name, owner_id, view, data_url, "
            + "calculate_histogram_metrics, samples_per_page, public, description) "
            + "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);",
            [
                project_config.uuid,
                project_config.name,
                owner_id,
                project_config.view,
                project_config.data_url,
                project_config.calculate_histogram_metrics,
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
                "data_type TEXT NOT NULL);"
            ).format(sql.Identifier(f"{project_config.uuid}_column_map"))
        )
        db.execute(
            sql.SQL(
                "INSERT INTO {} (column_id, name, type, data_type) "
                "VALUES (%s,%s,%s,%s);"
            ).format(sql.Identifier(f"{project_config.uuid}_column_map")),
            ["data_id", "data_id", ZenoColumnType.DATA, MetadataType.NOMINAL],
        )

        # Add metrics to the metrics table.
        for metric in project_config.metrics:
            db.execute(
                "INSERT INTO metrics (project_uuid, name, type, columns) VALUES "
                "(%s, %s, %s, %s);",
                [project_config.uuid, metric.name, metric.type, metric.columns],
            )

        # Create table to hold information about tags and associated datapoints.
        # db.execute(
        #     sql.SQL(
        #         "CREATE TABLE {}(id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY, "
        #         "tag_id integer NOT NULL REFERENCES tags(id) ON DELETE CASCADE "
        #         "ON UPDATE CASCADE, data_id text NOT NULL REFERENCES {}(data_id) "
        #         "ON DELETE CASCADE ON UPDATE CASCADE);"
        #     ).format(
        #         sql.Identifier(f"{project_config.uuid}_tags_datapoints"),
        #         sql.Identifier(project_config.uuid),
        #     )
        # )
        db.commit()


def dataset_schema(dataset_schema: DatasetSchema) -> list[str]:
    """Adding a dataset schema column_map to an existing project.

    Args:
        dataset_schema (DatasetSchema): the dataset schema to be added.

    Returns:
        list[str]: the ids of the columns in the dataset schema.
    """
    with Database() as db:
        db.execute(
            sql.SQL("DROP TABLE IF EXISTS {} CASCADE;").format(
                sql.Identifier(dataset_schema.project_uuid)
            )
        )
        db.execute(
            sql.SQL("DROP TABLE IF EXISTS {} CASCADE;").format(
                sql.Identifier(f"{dataset_schema.project_uuid}_column_map")
            )
        )
        db.commit()

    # Get column objects from the dataframe.
    columns: list[ZenoColumn] = []
    for col in dataset_schema.columns:
        column_type = ZenoColumnType.FEATURE
        if col == dataset_schema.id_column:
            column_type = ZenoColumnType.ID
        elif col == dataset_schema.label_column:
            column_type = ZenoColumnType.LABEL
        elif col == dataset_schema.data_column:
            column_type = ZenoColumnType.DATA
        elif col == dataset_schema.url_column:
            column_type = ZenoColumnType.DATA_URL

        columns.append(
            ZenoColumn(
                id=str(uuid.uuid4()),
                name=col,
                column_type=column_type,
                data_type=MetadataType.OTHER,
            )
        )

    with Database() as db:
        db.execute(
            sql.SQL(
                "CREATE TABLE {}(column_id TEXT NOT NULL PRIMARY KEY, "
                "name TEXT NOT NULL, type TEXT NOT NULL, model TEXT, "
                "data_type TEXT NOT NULL);"
            ).format(sql.Identifier(f"{dataset_schema.project_uuid}_column_map"))
        )
        for column in columns:
            db.execute(
                sql.SQL(
                    "INSERT INTO {} (column_id, name, type, data_type) "
                    "VALUES (%s,%s,%s,%s);"
                ).format(sql.Identifier(f"{dataset_schema.project_uuid}_column_map")),
                [column.id, column.name, column.column_type, column.data_type],
            )
        db.commit()

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
            await cursor.execute(
                sql.SQL("CREATE TABLE IF NOT EXISTS {} (").format(
                    sql.Identifier(project_uuid)
                )
                + cols
                + sql.SQL(")")
            )

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


def system(
    project: str,
    data_frame: pd.DataFrame,
    system_name: str,
    output_column: str,
    id_column: str,
):
    """Adds a system to an existing project.

    Args:
        project (str): project the user is currently working with.
        data_frame (pd.DataFrame): system data to be added.
        system_name (str): name of the system that produced the output.
        output_column (str): name of the column containing the system output.
        id_column (str): name of the column containing the instance IDs.
    """
    # Add all non-id and non-output columns to the column list.
    columns: list[ZenoColumn] = []
    for col in data_frame.columns:
        if col == id_column or col == output_column:
            continue
        columns.append(
            ZenoColumn(
                id=str(uuid.uuid4()),
                name=col,
                column_type=ZenoColumnType.FEATURE,
                data_type=resolve_metadata_type(data_frame, col),
                model=system_name,
            )
        )

    # Get column objects from the dataframe.
    output_col_object: ZenoColumn = ZenoColumn(
        id=str(uuid.uuid4()),
        name="output",
        column_type=ZenoColumnType.OUTPUT,
        data_type=MetadataType.NOMINAL,
        model=system_name,
    )
    # Create a renaming scheme for the DataFrame columns
    column_rename = {
        id_column: "data_id",
        output_column: output_col_object.id,
    }
    for col in columns:
        column_rename[col.name] = col.id
    data_frame = data_frame.rename(columns=column_rename)
    data_frame = data_frame.set_index("data_id")

    # Connect to the db engine using SQLAlchemy and write the data to a table.
    db = Database()
    config = config_db()
    engine = create_engine(
        f"postgresql+psycopg://{config['user']}:{config['password']}@{config['host']}/{config['dbname']}"
    )
    data_frame.to_sql("tmp", con=engine, if_exists="replace", index=True)
    columns.append(output_col_object)

    with Database() as db:
        # Check whether the system has the same columns as existing systems.
        system_columns = db.execute_return(
            sql.SQL("SELECT column_id, name FROM {} WHERE model IS NOT NULL;").format(
                sql.Identifier(f"{project}_column_map")
            )
        )
        system_column_names = list(set(map(lambda x: x[1], system_columns)))
        if len(system_column_names) > 0 and (
            len(columns) != len(system_column_names)
            or not all(map(lambda x: x.name in system_column_names, columns))
        ):
            raise Exception(
                "ERROR: The system you are trying to add does not have the same "
                "columns as existing systems."
            )

        # Check whether there are values for all data points.
        num_matches = db.execute_return(
            sql.SQL(
                "SELECT COUNT(*) FROM tmp JOIN {} ON tmp.data_id = {}.data_id;"
            ).format(sql.Identifier(project), sql.Identifier(project))
        )
        if num_matches[0][0] != len(data_frame.index):
            raise Exception(
                "ERROR: The system you are trying to add does not have values "
                "for all data points."
            )

        for col in columns:
            data_type = db.execute_return(
                sql.SQL(
                    "SELECT data_type FROM information_schema.columns WHERE "
                    "table_schema = 'public' AND table_name = 'tmp' AND "
                    "column_name = {};"
                ).format(sql.Literal(col.id))
            )

            db.execute(
                sql.SQL("ALTER TABLE {} ADD {} ").format(
                    sql.Identifier(project),
                    sql.Identifier(col.id),
                )
                + sql.SQL(data_type[0][0] + ";"),
            )
            db.execute(
                sql.SQL(
                    "UPDATE {} SET {} = (SELECT {} FROM tmp "
                    "WHERE tmp.data_id = {}.data_id)"
                ).format(
                    sql.Identifier(project),
                    sql.Identifier(col.id),
                    sql.Identifier(col.id),
                    sql.Identifier(project),
                )
            )
            db.execute(
                sql.SQL(
                    "INSERT INTO {} (column_id, name, type, data_type, model) "
                    "VALUES (%s,%s,%s,%s,%s);"
                ).format(sql.Identifier(f"{project}_column_map")),
                [col.id, col.name, col.column_type, col.data_type, col.model],
            )
        db.execute("DROP TABLE tmp;")
        db.commit()


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
        "INSERT INTO report_elements (report_id, type, data, chart_id, position)"
        " VALUES (%s,%s,%s,%s,%s) RETURNING id;",
        [report_id, element.type, element.data, element.chart_id, element.position],
    )
    if len(id) > 0:
        return id[0][0]


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
        'INSERT INTO users ("name") values(%s) RETURNING id;',
        [user.name],
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
            [user.id, id[0], True],
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
