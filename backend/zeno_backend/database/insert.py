"""Functions to insert new data into Zeno's database."""
import json
import uuid

from psycopg import DatabaseError, sql

from zeno_backend.classes.base import (
    FeatureSpec,
    LabelSpec,
    MetadataType,
    OutputSpec,
    PostdistillSpec,
    Project,
    ZenoColumnType,
)
from zeno_backend.classes.chart import Chart, ParametersEncoder
from zeno_backend.classes.filter import PredicatesEncoder
from zeno_backend.classes.slice import Slice
from zeno_backend.classes.tag import Tag
from zeno_backend.classes.user import Organization, User
from zeno_backend.database.database import Database


def setup_project(description: Project, user: User):
    """Setting up a new project in Zeno.

    Creates a new entry in the projects table, creates a new table for the project's
    data, creates a table to map data columns to ids and types, and creates a table for
    all tags of the project.

    Args:
        description (ProjectConfig): the configuration with which to initialize the new
        project.
        user (User): the user who is setting up the project and becomes its admin.

    Raises:
        Exception: something went wrong in the process of creating the new project in
        the database.
    """
    db = Database()
    try:
        db.connect()
        db.execute(
            "INSERT INTO projects (uuid, name, view, calculate_histogram_metrics, "
            "num_items, public) VALUES (%s,%s,%s,%s,%s,%s);",
            [
                description.uuid,
                description.name,
                description.view,
                description.calculate_histogram_metrics,
                description.num_items,
                description.public,
            ],
        )
        db.execute(
            "INSERT INTO user_project (user_id, project_uuid, editor) "
            "VALUES (%s,%s,%s)",
            [user.id, description.uuid, True],
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
                "CREATE TABLE {}(id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY, "
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


def feature(feature_spec: FeatureSpec, project: str):
    """Adds a feature to an item in the project's databse.

    Args:
        feature_spec: the specification of the feature function.
        project (str): the project the user is currently working with.

    Raises:
        Exception: something went wrong while inserting the feature into the
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
                feature_spec.col_name,
                ZenoColumnType.FEATURE,
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
                    ZenoColumnType.FEATURE,
                    feature_spec.type,
                    feature_spec.col_name,
                ],
            )
            db.execute(
                sql.SQL("ALTER TABLE {} ADD {} " + str(feature_spec.type) + ";").format(
                    sql.Identifier(project),
                    sql.Identifier(col_uuid),
                )
            )
        else:
            col_uuid = str(exists[0])
        db.execute(
            sql.SQL("UPDATE {} SET {} = %s WHERE item = %s;").format(
                sql.Identifier(project), sql.Identifier(col_uuid)
            ),
            [feature_spec.value, feature_spec.item],
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
                sql.SQL(
                    "ALTER TABLE {} ADD {} " + str(postdistill_spec.type) + ";"
                ).format(
                    sql.Identifier(project),
                    sql.Identifier(col_uuid),
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
        'INSERT INTO users ("name") values(%s)',
        [user.name],
    )


def organization(user: User, organization: Organization):
    """Add a new organization to the database.

    Args:
        user (User): the user who created the organization.
        organization (Organization): the organization to be created.
    """
    db = Database()
    try:
        db.connect()
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
    except (Exception, DatabaseError) as error:
        raise Exception(error) from error
    finally:
        db.disconnect()


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
