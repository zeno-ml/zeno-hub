"""Functions to insert new data into Zeno's database."""
import json
import uuid

from psycopg import DatabaseError, sql

from zeno_backend.classes.base import (
    LabelSpec,
    MetadataType,
    OutputSpec,
    PostdistillSpec,
    PredistillSpec,
    ProjectConfig,
    ZenoColumnType,
)
from zeno_backend.classes.chart import Chart, ParametersEncoder
from zeno_backend.classes.filter import PredicatesEncoder
from zeno_backend.classes.slice import Slice
from zeno_backend.classes.tag import Tag
from zeno_backend.classes.user import User
from zeno_backend.database.database import Database


def setup_project(description: ProjectConfig):
    """Setting up a new project in Zeno.

    Creates a new entry in the projects table, creates a new table for the project's
    data, creates a table to map data columns to ids and types, and creates a table for
    all tags of the project.

    Args:
        description (ProjectConfig): the configuration with which to initialize the new
        project.

    Raises:
        Exception: something went wrong in the process of creating the new project in
        the database.
    """
    db = Database()
    try:
        db.connect()
        db.execute(
            'INSERT INTO projects ("uuid", "name", "view") VALUES (%s,%s,%s);',
            [description.uuid, description.name, description.view],
        )
        db.execute(
            sql.SQL("CREATE TABLE {}(item TEXT NOT NULL PRIMARY KEY);").format(
                sql.Identifier(description.uuid)
            )
        )
        db.execute(
            sql.SQL(
                "CREATE TABLE {}(column_id TEXT NOT NULL PRIMARY KEY, "
                "name TEXT NOT NULL, type TEXT NOT NULL, model TEXT, "
                "data_type TEXT NOT NULL);"
            ).format(sql.Identifier(f"{description.uuid}_column_map"))
        )
        db.execute(
            sql.SQL(
                "INSERT INTO {} (column_id, name, type, data_type) "
                "VALUES (%s,%s,%s,%s);"
            ).format(sql.Identifier(f"{description.uuid}_column_map")),
            ["item", "item", ZenoColumnType.ITEM, MetadataType.NOMINAL],
        )
        db.execute(
            sql.SQL(
                "CREATE TABLE {}(id INTEGER NOT NULL PRIMARY KEY, "
                "tag_id integer NOT NULL REFERENCES tags(id) ON DELETE CASCADE "
                "ON UPDATE CASCADE, item_id text NOT NULL REFERENCES {}(item) "
                "ON DELETE CASCADE ON UPDATE CASCADE);"
            ).format(
                sql.Identifier(f"{description.uuid}_tags_items"),
                sql.Identifier(description.uuid),
            )
        )
        db.commit()
    except (Exception, DatabaseError) as error:
        raise Exception(error) from error
    finally:
        db.disconnect()


def item(name: str, project: str):
    """Adds a new data item to an existing project.

    Args:
        name (str): name of the item to be added to the project data.
        project (str): the project the user is currently working with.
    """
    db = Database()
    db.connect_execute(
        sql.SQL('INSERT INTO {} ("item") VALUES (%s);').format(sql.Identifier(project)),
        [
            name,
        ],
    )


def label(label_spec: LabelSpec, project: str):
    """Adds a label to an item in the project's databse.

    Args:
        label_spec (LabelSpec): the specification of the label to be added.
        project (str): the project the user is currently working with.

    Raises:
        Exception: something went wrong while inserting the label into the database.
    """
    db = Database()
    try:
        db.connect()
        exists = db.execute_return(
            sql.SQL("SELECT COUNT(1) FROM {} WHERE column_id = 'label'").format(
                sql.Identifier(f"{project}_column_map")
            )
        )
        if exists is not None and exists[0] == 0:
            db.execute(
                sql.SQL(
                    "INSERT INTO {} (column_id, name, type, data_type) "
                    "VALUES (%s,%s,%s,%s);"
                ).format(sql.Identifier(f"{project}_column_map")),
                ["label", "label", ZenoColumnType.LABEL, MetadataType.NOMINAL],
            )
            db.execute(
                sql.SQL("ALTER TABLE {} ADD label TEXT;").format(
                    sql.Identifier(project)
                )
            )
        db.execute(
            sql.SQL("UPDATE {} SET label = %s WHERE item = %s;").format(
                sql.Identifier(project)
            ),
            [label_spec.label, label_spec.item],
        )
        db.commit()
    except (Exception, DatabaseError) as error:
        raise Exception(error) from error
    finally:
        db.disconnect()


def output(output_spec: OutputSpec, project: str):
    """Adds a model output to an item in the project's databse.

    Args:
        output_spec (OutputSpec): the specification of the output to be added.
        project (str): the project the user is currently working with.

    Raises:
        Exception: something went wrong while inserting the output into the database.
    """
    db = Database()
    try:
        db.connect()
        exists = db.execute_return(
            sql.SQL("SELECT * FROM {} WHERE model = %s AND type = %s").format(
                sql.Identifier(f"{project}_column_map")
            ),
            [output_spec.model, ZenoColumnType.OUTPUT],
        )
        col_uuid: str = str(uuid.uuid4())
        if exists is None:
            db.execute(
                sql.SQL(
                    "INSERT INTO {} (column_id, name, type, data_type, model) "
                    "VALUES (%s,%s,%s,%s,%s);"
                ).format(sql.Identifier(f"{project}_column_map")),
                [
                    col_uuid,
                    "output",
                    ZenoColumnType.OUTPUT,
                    MetadataType.NOMINAL,
                    output_spec.model,
                ],
            )
            db.execute(
                sql.SQL("ALTER TABLE {} ADD {} TEXT;").format(
                    sql.Identifier(project), sql.Identifier(col_uuid)
                )
            )
        else:
            col_uuid = str(exists[0])
        db.execute(
            sql.SQL("UPDATE {} SET {} = %s WHERE item = %s;").format(
                sql.Identifier(project), sql.Identifier(col_uuid)
            ),
            [output_spec.output, output_spec.item],
        )
        db.commit()
    except (Exception, DatabaseError) as error:
        raise Exception(error) from error
    finally:
        db.disconnect()


def predistill(predistill_spec: PredistillSpec, project: str):
    """Adds a predistill result to an item in the project's databse.

    Args:
        predistill_spec (PredistillSpec): the specification of the predistill
        calculation to be added.
        project (str): the project the user is currently working with.

    Raises:
        Exception: something went wrong while inserting the predistill data into the
        database.
    """
    db = Database()
    try:
        db.connect()
        exists = db.execute_return(
            sql.SQL("SELECT * FROM {} WHERE name = %s AND type = %s").format(
                sql.Identifier(f"{project}_column_map")
            ),
            [
                predistill_spec.col_name,
                ZenoColumnType.PREDISTILL,
            ],
        )
        col_uuid: str = str(uuid.uuid4())
        if exists is None:
            db.execute(
                sql.SQL(
                    "INSERT INTO {} (column_id, type, data_type, name) "
                    "VALUES (%s,%s,%s,%s);"
                ).format(sql.Identifier(f"{project}_column_map")),
                [
                    col_uuid,
                    ZenoColumnType.PREDISTILL,
                    predistill_spec.type,
                    predistill_spec.col_name,
                ],
            )
            db.execute(
                sql.SQL("ALTER TABLE {} ADD {} {};").format(
                    sql.Identifier(project),
                    sql.Identifier(col_uuid),
                    sql.Literal(str(predistill_spec.type)),
                )
            )
        else:
            col_uuid = str(exists[0])
        db.execute(
            sql.SQL("UPDATE {} SET {} = %s WHERE item = %s;").format(
                sql.Identifier(project), sql.Identifier(col_uuid)
            ),
            [predistill_spec.value, predistill_spec.item],
        )
        db.commit()
    except (Exception, DatabaseError) as error:
        raise Exception(error) from error
    finally:
        db.disconnect()


def postdistill(postdistill_spec: PostdistillSpec, project: str):
    """Adds a postdistill result to an item in the project's databse.

    Args:
        postdistill_spec (PostdistillSpec): the specification of the postdistill
        calculation to be added.
        project (str): the project the user is currently working with.

    Raises:
        Exception: something went wrong while inserting the postdistill data into the
        database.
    """
    db = Database()
    try:
        db.connect()
        exists = db.execute_return(
            sql.SQL(
                "SELECT * FROM {} WHERE name = %s AND type = %s AND model = %s"
            ).format(sql.Identifier(f"{project}_column_map")),
            [
                postdistill_spec.col_name,
                ZenoColumnType.POSTDISTILL,
                postdistill_spec.model,
            ],
        )
        col_uuid: str = str(uuid.uuid4())
        if exists is None:
            db.execute(
                sql.SQL(
                    "INSERT INTO {} (column_id, type, data_type, name, model) "
                    "VALUES (%s,%s,%s,%s,%s);"
                ).format(sql.Identifier(f"{project}_column_map")),
                [
                    col_uuid,
                    ZenoColumnType.POSTDISTILL,
                    postdistill_spec.type,
                    postdistill_spec.col_name,
                    postdistill_spec.model,
                ],
            )
            db.execute(
                sql.SQL("ALTER TABLE {} ADD {} {};").format(
                    sql.Identifier(project),
                    sql.Identifier(col_uuid),
                    sql.Literal(str(postdistill_spec.type)),
                )
            )
        else:
            col_uuid = str(exists[0])
        db.execute(
            sql.SQL("UPDATE {} SET {} = %s WHERE item = %s;").format(
                sql.Identifier(project), sql.Identifier(col_uuid)
            ),
            [postdistill_spec.value, postdistill_spec.item],
        )
        db.commit()
    except (Exception, DatabaseError) as error:
        raise Exception(error) from error
    finally:
        db.disconnect()


def folder(project: str, name: str):
    """Adding a folder to an existing project.

    Args:
        project (str): the project the user is currently working with.
        name (str): name of the folder to be added.
    """
    db = Database()
    db.connect_execute(
        "INSERT INTO folders (name, project_uuid) VALUES (%s,%s);",
        [name, project],
    )


def slice(project: str, req: Slice):
    """Add a slice to an existing project.

    Args:
        project (str): the project the user is currently working with.
        req (Slice): the slice to be added to the project.
    """
    db = Database()
    db.connect_execute(
        "INSERT INTO slices (name, folder_id, filter, project_uuid) "
        "VALUES (%s,%s,%s,%s);",
        [
            req.slice_name,
            req.folder_id,
            json.dumps(req.filter_predicates, cls=PredicatesEncoder),
            project,
        ],
    )


def chart(project: str, chart: Chart):
    """Add a chart to an existing project.

    Args:
        project (str): the project the user is currently working with.
        chart (Chart): the chart to be added to the project.
    """
    db = Database()
    db.connect_execute(
        "INSERT INTO charts (name, type, parameters, project_uuid) "
        "VALUES (%s,%s,%s,%s);",
        [
            chart.name,
            chart.type,
            json.dumps(chart.parameters, cls=ParametersEncoder),
            project,
        ],
    )


def tag(project: str, tag: Tag):
    """Add a tag to an existing project.

    Args:
        project (str): the project the user is currently working with.
        tag (Tag): the tag to be added to the project.
    """
    db = Database()
    try:
        db.connect()
        id = db.execute_return(
            "INSERT INTO tags (name, folder_id, project_uuid) VALUES (%s,%s,%s) "
            "RETURNING id;",
            [tag.tag_name, tag.folder_id, project],
        )
        if id is None:
            return
        for item in tag.items:
            db.execute(
                sql.SQL("INSERT INTO {} (tag_id, item_id) VALUES (%s,%s);").format(
                    sql.Identifier(f"{project}_tags_items")
                ),
                [id[0], item],
            )
        db.commit()
    except (Exception, DatabaseError) as error:
        raise Exception(error) from error
    finally:
        db.disconnect()


def user(user: User):
    """Add a new user to the database.

    Args:
        user (User): the user to be added.
    """
    db = Database()
    db.connect_execute(
        'INSERT INTO users ("user_name","email","secret") values(%s,%s,%s)',
        [user.name, user.email, user.secret],
    )
