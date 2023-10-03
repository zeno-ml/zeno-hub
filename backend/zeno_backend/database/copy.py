"""Functionality for copying instances in the database."""
import uuid

from psycopg import sql

import zeno_backend.database.select as select
from zeno_backend.classes.project import ProjectCopy
from zeno_backend.classes.user import User
from zeno_backend.database.database import Database


def project_copy(project_uuid: str, copy_spec: ProjectCopy, user: User):
    """Copy a project.

    Args:
        project_uuid (str): UUID of the project to copy.
        copy_spec (ProjectCopy): specification of the copy process.
        user (User): user who is copying the project.

    Raises:
        Exception: something went wrong in the process of copying a project in
            the database.
    """
    if select.project_exists(user.id, copy_spec.name) and user.name is not None:
        raise Exception("Project with this name already exists.")

    with Database() as db:
        # Get project to copy from.
        project_result = db.execute_return(
            "SELECT uuid, name, view, data_url, calculate_histogram_metrics, "
            "samples_per_page, public, description FROM projects WHERE uuid = %s;",
            [project_uuid],
        )
        if len(project_result) == 0:
            raise Exception("Project does not exist.")

        # Create new project in DB.
        new_uuid = str(uuid.uuid4())
        db.execute(
            "INSERT INTO projects (uuid, name, owner_id, view, data_url, "
            + "calculate_histogram_metrics, samples_per_page, public, description) "
            + "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);",
            [
                new_uuid,
                copy_spec.name,
                user.id,
                str(project_result[0][2]),
                copy_spec.data_url
                if copy_spec.data_url is not None
                else str(project_result[0][3]),
                bool(project_result[0][4]),
                project_result[0][5] if isinstance(project_result[0][5], int) else 10,
                False,
                str(project_result[0][7]),
            ],
        )
        db.execute(
            "INSERT INTO user_project (user_id, project_uuid, editor) "
            "VALUES (%s,%s,%s)",
            [user.id, new_uuid, True],
        )

        # Copy metrics.
        db.execute(
            sql.SQL(
                "INSERT INTO metrics (project_uuid, name, type, columns) (SELECT "
                "{} as uuid, name, type, columns FROM metrics WHERE project_uuid = %s);"
            ).format(sql.Literal(new_uuid)),
            [project_uuid],
        )

        db.execute(
            sql.SQL(
                "CREATE TABLE {}(column_id TEXT NOT NULL PRIMARY KEY, "
                "name TEXT NOT NULL, type TEXT NOT NULL, model TEXT, "
                "data_type TEXT NOT NULL);"
            ).format(sql.Identifier(f"{new_uuid}_column_map"))
        )

        if not copy_spec.copy_data:
            db.commit()
            return

        if not copy_spec.copy_systems:
            # Copy data schema.
            db.execute(
                sql.SQL(
                    "INSERT INTO {} (column_id, name, type, data_type) (SELECT "
                    "column_id, name, type, data_type FROM {} WHERE model is NULL);"
                ).format(
                    sql.Identifier(f"{new_uuid}_column_map"),
                    sql.Identifier(f"{project_uuid}_column_map"),
                ),
            )
            copy_data(db, project_uuid, new_uuid)
            return

        # Copy data and systems schema.
        db.execute(
            sql.SQL(
                "INSERT INTO {} (column_id, name, type, data_type) (SELECT "
                "column_id, name, type, data_type FROM {});"
            ).format(
                sql.Identifier(f"{new_uuid}_column_map"),
                sql.Identifier(f"{project_uuid}_column_map"),
            ),
        )
        copy_data(db, project_uuid, new_uuid)

        if not copy_spec.copy_slices:
            return

        # Copy slices.
        db.execute(
            sql.SQL(
                "INSERT INTO slices (name, filter, project_uuid) (SELECT "
                "name, filter, {} as uuid FROM slices WHERE project_uuid = %s);"
            ).format(sql.Literal(new_uuid)),
            [project_uuid],
        )

        if not copy_spec.copy_charts:
            return

        # Copy charts.
        db.execute(
            sql.SQL(
                "INSERT INTO charts (name, type, parameters, project_uuid) (SELECT "
                "name, type, parameters, {} as uuid FROM charts "
                "WHERE project_uuid = %s);"
            ).format(sql.Literal(new_uuid)),
            [project_uuid],
        )


def copy_data(db: Database, old_uuid: str, new_uuid: str):
    """Copy data from one table to another.

    Args:
        db (Database): the database to copy data in.
        old_uuid (str): uuid of the old table.
        new_uuid (str): uuid of the new table.
    """
    columns_request = db.execute_return(
        sql.SQL("SELECT column_id FROM {};").format(
            sql.Identifier(f"{new_uuid}_column_map")
        )
    )
    if len(columns_request) > 0:
        columns = [column[0] for column in columns_request]
        cols = sql.SQL(",").join([sql.Identifier(col) for col in columns])
        db.execute(
            sql.SQL("CREATE TABLE {} AS (SELECT ").format(sql.Identifier(new_uuid))
            + cols
            + sql.SQL(" FROM {});").format(sql.Identifier(old_uuid))
        )
        db.commit()

    # Get ID column name
    col_id = db.execute_return(
        sql.SQL("SELECT column_id FROM {} WHERE type = 'ID';").format(
            sql.Identifier(f"{new_uuid}_column_map")
        )
    )
    if len(col_id) == 0:
        raise Exception("ERROR: No ID column found.")
    col_id = col_id[0][0]

    # Make ID column primary key.
    db.execute(
        sql.SQL("ALTER TABLE {} ADD PRIMARY KEY ({});").format(
            sql.Identifier(new_uuid),
            sql.Identifier(col_id),
        )
    )

    # Create table to hold information about tags and associated datapoints.
    db.execute(
        sql.SQL(
            "CREATE TABLE {}(id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY, "
            "tag_id integer NOT NULL REFERENCES tags(id) ON DELETE CASCADE "
            "ON UPDATE CASCADE, data_id text NOT NULL REFERENCES {}({}) "
            "ON DELETE CASCADE ON UPDATE CASCADE);"
        ).format(
            sql.Identifier(f"{new_uuid}_tags_datapoints"),
            sql.Identifier(new_uuid),
            sql.Identifier(col_id),
        )
    )
