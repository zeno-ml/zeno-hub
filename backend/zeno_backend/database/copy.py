"""Functionality for copying instances in the database."""
import json
import uuid

from psycopg import AsyncConnection, AsyncCursor, sql

import zeno_backend.database.select as select
from zeno_backend.classes.project import ProjectCopy
from zeno_backend.classes.user import User
from zeno_backend.database.database import db_pool


async def project_copy(project_uuid: str, copy_spec: ProjectCopy, user: User):
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

    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            # Get project to copy from.
            await cur.execute(
                "SELECT uuid, name, view, samples_per_page, public, "
                "description FROM projects WHERE uuid = %s;",
                [project_uuid],
            )
            project_result = await cur.fetchall()
            if len(project_result) == 0:
                raise Exception("Project does not exist.")

            # Create new project in DB.
            new_uuid = str(uuid.uuid4())
            await cur.execute(
                "INSERT INTO projects (uuid, name, owner_id, view, "
                + "samples_per_page, public, description) "
                + "VALUES (%s,%s,%s,%s,%s,%s,%s);",
                [
                    new_uuid,
                    copy_spec.name,
                    user.id,
                    str(project_result[0][2]),
                    project_result[0][3]
                    if isinstance(project_result[0][3], int)
                    else 10,
                    False,
                    str(project_result[0][5]),
                ],
            )
            await cur.execute(
                "INSERT INTO user_project (user_id, project_uuid, editor) "
                "VALUES (%s,%s,%s)",
                [user.id, new_uuid, True],
            )

            # Copy metrics.
            await cur.execute(
                sql.SQL(
                    "INSERT INTO metrics (project_uuid, name, type, columns) (SELECT {}"
                    "as uuid, name, type, columns FROM metrics WHERE project_uuid = %s)"
                ).format(sql.Literal(new_uuid)),
                [project_uuid],
            )

            await cur.execute(
                sql.SQL(
                    "CREATE TABLE {}(column_id TEXT NOT NULL PRIMARY KEY, "
                    "name TEXT NOT NULL, type TEXT NOT NULL, model TEXT, "
                    "data_type TEXT NOT NULL, histogram jsonb);"
                ).format(sql.Identifier(f"{new_uuid}_column_map"))
            )

            if not copy_spec.copy_data:
                await conn.commit()
                return

            if not copy_spec.copy_systems:
                # Copy data schema.
                await cur.execute(
                    sql.SQL(
                        "INSERT INTO {} (column_id, name, type, data_type, histogram) "
                        "(SELECT column_id, name, type, data_type, histogram FROM {} "
                        "WHERE model is NULL); "
                    ).format(
                        sql.Identifier(f"{new_uuid}_column_map"),
                        sql.Identifier(f"{project_uuid}_column_map"),
                    ),
                )
                await copy_data(cur, conn, project_uuid, new_uuid)
                return

            # Copy data and systems schema.
            await cur.execute(
                sql.SQL(
                    "INSERT INTO {} (column_id, name, type, model, data_type, histogram"
                    ") (SELECT column_id, name, type, model, data_type, histogram FROM "
                    "{})"
                ).format(
                    sql.Identifier(f"{new_uuid}_column_map"),
                    sql.Identifier(f"{project_uuid}_column_map"),
                ),
            )
            if not copy_spec.copy_slices:
                await copy_data(cur, conn, project_uuid, new_uuid)
                return

            # Copy slices.
            await cur.execute(
                sql.SQL(
                    "INSERT INTO slices (name, folder_id, filter, project_uuid) (SELECT"
                    " name, folder_id, filter, {} as uuid FROM slices "
                    "WHERE project_uuid = %s);"
                ).format(sql.Literal(new_uuid)),
                [project_uuid],
            )

            # Copy folders and add slices.
            await cur.execute(
                "SELECT id, name FROM folders WHERE project_uuid = %s;", [project_uuid]
            )
            folders = await cur.fetchall()
            for folder in folders:
                await cur.execute(
                    "INSERT INTO folders (name, project_uuid) VALUES (%s, %s) "
                    "RETURNING id;",
                    [folder[1], new_uuid],
                )
                id = await cur.fetchall()
                await cur.execute(
                    "UPDATE slices SET folder_id = %s WHERE folder_id = %s "
                    "AND project_uuid = %s;",
                    [id[0][0], folder[0], new_uuid],
                )

            if not copy_spec.copy_charts:
                await copy_data(cur, conn, project_uuid, new_uuid)
                return

            await copy_charts(cur, conn, project_uuid, new_uuid)
            await copy_data(cur, conn, project_uuid, new_uuid)


async def copy_data(
    cur: AsyncCursor, conn: AsyncConnection, old_uuid: str, new_uuid: str
):
    """Copy data from one table to another.

    Args:
        cur (AsyncCursor): cursor to execute SQL commands.
        conn (AsyncConnection): connection to the database.
        old_uuid (str): uuid of the old table.
        new_uuid (str): uuid of the new table.
    """
    await cur.execute(
        sql.SQL("SELECT column_id FROM {};").format(
            sql.Identifier(f"{new_uuid}_column_map")
        )
    )
    columns_request = await cur.fetchall()
    if len(columns_request) > 0:
        columns = [column[0] for column in columns_request]
        cols = sql.SQL(",").join([sql.Identifier(col) for col in columns])
        await cur.execute(
            sql.SQL("CREATE TABLE {} AS (SELECT ").format(sql.Identifier(new_uuid))
            + cols
            + sql.SQL(" FROM {});").format(sql.Identifier(old_uuid))
        )
        await conn.commit()

    # Get ID column name
    await cur.execute(
        sql.SQL("SELECT column_id FROM {} WHERE type = 'ID';").format(
            sql.Identifier(f"{new_uuid}_column_map")
        )
    )
    col_id = await cur.fetchall()
    if len(col_id) == 0:
        raise Exception("ERROR: No ID column found.")
    col_id = col_id[0][0]

    # Make ID column primary key.
    await cur.execute(
        sql.SQL("ALTER TABLE {} ADD PRIMARY KEY ({});").format(
            sql.Identifier(new_uuid),
            sql.Identifier(col_id),
        )
    )

    # Create table to hold information about tags and associated datapoints.
    await cur.execute(
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
    await conn.commit()


async def copy_charts(
    cur: AsyncCursor, conn: AsyncConnection, old_uuid: str, new_uuid: str
):
    """Copy charts from one project to another.

    Args:
        cur (AsyncCursor): cursor to execute SQL commands.
        conn (AsyncConnection): connection to the database.
        old_uuid (str): uuid of the old project.
        new_uuid (str): uuid of the new project.
    """
    # Copy charts.
    await cur.execute(
        sql.SQL(
            "INSERT INTO charts (name, type, parameters, project_uuid) (SELECT "
            "name, type, parameters, {} as uuid FROM charts "
            "WHERE project_uuid = %s);"
        ).format(sql.Literal(new_uuid)),
        [old_uuid],
    )

    # Get chart parameters.
    await cur.execute(
        "SELECT id, parameters FROM charts WHERE project_uuid = %s;",
        [new_uuid],
    )
    params = await cur.fetchall()

    # Update chart slices and metrics.
    if len(params) > 0:
        for params_element in params:
            json_params = json.loads(params_element[1])
            if "slices" in json_params:
                for i, slice_id in enumerate(json_params["slices"]):
                    json_params["slices"][i] = await resolve_slice(
                        cur, new_uuid, slice_id
                    )
            if "x_values" in json_params:
                for i, x_value in enumerate(json_params["x_values"]):
                    json_params["x_values"][i] = await resolve_slice(
                        cur, new_uuid, x_value
                    )
            if "y_values" in json_params:
                for i, y_value in enumerate(json_params["y_values"]):
                    json_params["y_values"][i] = await resolve_slice(
                        cur, new_uuid, y_value
                    )
            if "metrics" in json_params:
                for i, metric in enumerate(json_params["metrics"]):
                    json_params["metrics"][i] = await resolve_metric(
                        cur, new_uuid, metric
                    )
            if "metric" in json_params:
                json_params["metric"] = await resolve_metric(
                    cur, new_uuid, json_params["metric"]
                )
            await cur.execute(
                "UPDATE charts SET parameters = %s WHERE id = %s;",
                [json.dumps(json_params), params_element[0]],
            )


async def resolve_slice(cur: AsyncCursor, new_uuid: str, slice_id: int):
    """Map a slice_id from an old project to a slice_id in a new project.

    Args:
        cur (AsyncCursor): cursor to execute SQL commands.
        new_uuid (str): uuid of the new project.
        slice_id (int): id of the slice in the old project.
    """
    # All instances slice
    if slice_id == -1:
        return slice_id

    await cur.execute("SELECT name FROM slices WHERE id = %s;", [slice_id])
    slice_name = await cur.fetchall()
    if len(slice_name) == 0:
        return None
    slice_name = slice_name[0][0]
    await cur.execute(
        "SELECT id FROM slices WHERE name = %s AND project_uuid = %s;",
        [slice_name, new_uuid],
    )
    new_id = await cur.fetchall()
    if len(new_id) == 0:
        return None
    return new_id[0][0]


async def resolve_metric(cur: AsyncCursor, new_uuid: str, metric_id: int):
    """Map a metric_id from an old project to a metric_id in a new project.

    Args:
        cur (AsyncCursor): cursor to execute SQL commands.
        new_uuid (str): uuid of the new project.
        metric_id (int): id of the metric in the old project.
    """
    # Num_instances metric
    if metric_id == -1:
        return metric_id

    await cur.execute("SELECT name FROM metrics WHERE id = %s;", [metric_id])
    metric_name = await cur.fetchall()
    if len(metric_name) == 0:
        return None
    metric_name = metric_name[0][0]
    await cur.execute(
        "SELECT id FROM metrics WHERE name = %s AND project_uuid = %s;",
        [metric_name, new_uuid],
    )
    new_id = await cur.fetchall()
    if len(new_id) == 0:
        return None
    return new_id[0][0]
