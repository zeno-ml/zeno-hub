"""Functionality for copying instances in the database."""
import json
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
            "SELECT uuid, name, view, samples_per_page, public, "
            "description FROM projects WHERE uuid = %s;",
            [project_uuid],
        )
        if len(project_result) == 0:
            raise Exception("Project does not exist.")

        # Create new project in DB.
        new_uuid = str(uuid.uuid4())
        db.execute(
            "INSERT INTO projects (uuid, name, owner_id, view, "
            + "samples_per_page, public, description) "
            + "VALUES (%s,%s,%s,%s,%s,%s,%s);",
            [
                new_uuid,
                copy_spec.name,
                user.id,
                str(project_result[0][2]),
                project_result[0][3] if isinstance(project_result[0][3], int) else 10,
                False,
                str(project_result[0][5]),
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
                "data_type TEXT NOT NULL, histogram jsonb);"
            ).format(sql.Identifier(f"{new_uuid}_column_map"))
        )

        if not copy_spec.copy_data:
            db.commit()
            return

        if not copy_spec.copy_systems:
            # Copy data schema.
            db.execute(
                sql.SQL(
                    "INSERT INTO {} (column_id, name, type, data_type, histogram) "
                    "(SELECT column_id, name, type, data_type, histogram FROM {} "
                    "WHERE model is NULL); "
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
                "INSERT INTO {} (column_id, name, type, model, data_type, histogram) "
                "(SELECT column_id, name, type, model, data_type, histogram FROM {});"
            ).format(
                sql.Identifier(f"{new_uuid}_column_map"),
                sql.Identifier(f"{project_uuid}_column_map"),
            ),
        )
        if not copy_spec.copy_slices:
            copy_data(db, project_uuid, new_uuid)
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
            copy_data(db, project_uuid, new_uuid)
            return

        copy_charts(db, project_uuid, new_uuid)
        copy_data(db, project_uuid, new_uuid)


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
    db.commit()


def copy_charts(db: Database, old_uuid: str, new_uuid: str):
    """Copy charts from one project to another.

    Args:
        db (Database): the database to copy data in.
        old_uuid (str): uuid of the old project.
        new_uuid (str): uuid of the new project.
    """
    # Copy charts.
    db.execute(
        sql.SQL(
            "INSERT INTO charts (name, type, parameters, project_uuid) (SELECT "
            "name, type, parameters, {} as uuid FROM charts "
            "WHERE project_uuid = %s);"
        ).format(sql.Literal(new_uuid)),
        [old_uuid],
    )

    # Get chart parameters.
    params = db.execute_return(
        "SELECT id, parameters FROM charts WHERE project_uuid = %s;",
        [new_uuid],
    )

    # Update chart slices and metrics.
    if len(params) > 0:
        for params_element in params:
            json_params = json.loads(params_element[1])
            if "slices" in json_params:
                json_params["slices"] = list(
                    map(lambda x: resolve_slice(db, new_uuid, x), json_params["slices"])
                )
            if "x_values" in json_params:
                json_params["x_values"] = list(
                    map(
                        lambda x: resolve_slice(db, new_uuid, x)
                        if isinstance(x, int)
                        else x,
                        json_params["y_values"],
                    )
                )
            if "y_values" in json_params:
                json_params["y_values"] = list(
                    map(
                        lambda x: resolve_slice(db, new_uuid, x)
                        if isinstance(x, int)
                        else x,
                        json_params["y_values"],
                    )
                )
            if "metrics" in json_params:
                json_params["metrics"] = list(
                    map(
                        lambda x: resolve_metric(db, new_uuid, x),
                        json_params["metrics"],
                    )
                )
            if "metric" in json_params:
                json_params["metric"] = resolve_metric(
                    db, new_uuid, json_params["metric"]
                )
            db.execute(
                "UPDATE charts SET parameters = %s WHERE id = %s;",
                [json.dumps(json_params), params_element[0]],
            )


def resolve_slice(db: Database, new_uuid: str, slice_id: int):
    """Map a slice_id from an old project to a slice_id in a new project.

    Args:
        db (Database): the database to copy data in.
        new_uuid (str): uuid of the new project.
        slice_id (int): id of the slice in the old project.
    """
    # All instances slice
    if slice_id == -1:
        return slice_id

    slice_name = db.execute_return("SELECT name FROM slices WHERE id = %s;", [slice_id])
    if len(slice_name) == 0:
        return None
    slice_name = slice_name[0][0]
    new_id = db.execute_return(
        "SELECT id FROM slices WHERE name = %s AND project_uuid = %s;",
        [slice_name, new_uuid],
    )
    if len(new_id) == 0:
        return None
    return new_id[0][0]


def resolve_metric(db: Database, new_uuid: str, metric_id: int):
    """Map a metric_id from an old project to a metric_id in a new project.

    Args:
        db (Database): the database to copy data in.
        new_uuid (str): uuid of the new project.
        metric_id (int): id of the metric in the old project.
    """
    # Num_instances metric
    if metric_id == -1:
        return metric_id

    metric_name = db.execute_return(
        "SELECT name FROM metrics WHERE id = %s;", [metric_id]
    )
    if len(metric_name) == 0:
        return None
    metric_name = metric_name[0][0]
    new_id = db.execute_return(
        "SELECT id FROM metrics WHERE name = %s AND project_uuid = %s;",
        [metric_name, new_uuid],
    )
    if len(new_id) == 0:
        return None
    return new_id[0][0]
