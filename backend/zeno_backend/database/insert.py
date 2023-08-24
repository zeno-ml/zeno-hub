"""Functions to insert new data into Zeno's database."""
import json
import uuid

import pandas as pd
from psycopg import sql
from sqlalchemy import create_engine

from zeno_backend.classes.base import MetadataType, ZenoColumn, ZenoColumnType
from zeno_backend.classes.chart import Chart, ParametersEncoder
from zeno_backend.classes.filter import PredicatesEncoder
from zeno_backend.classes.project import Project
from zeno_backend.classes.slice import Slice
from zeno_backend.classes.tag import Tag
from zeno_backend.classes.user import Organization, User
from zeno_backend.database.database import Database
from zeno_backend.database.util import resolve_metadata_type


def project(project_config: Project, user: User):
    """Setting up a new project in Zeno.

    Creates a new entry in the projects table, creates a new table for the project's
    data, creates a table to map data columns to ids and types, and creates a table for
    all tags of the project.

    Args:
        project_config (Project): the configuration with which to
            initialize the new project.
        user (User): the user who is setting up the project and becomes its admin.

    Raises:
        Exception: something went wrong in the process of creating the new project in
        the database.
    """
    with Database() as db:
        db.execute(
            "INSERT INTO projects (uuid, name, owner_id, view, data_url, "
            + "calculate_histogram_metrics, samples_per_page, public) "
            + "VALUES (%s,%s,%s,%s,%s,%s,%s,%s);",
            [
                project_config.uuid,
                project_config.name,
                user.id,
                project_config.view,
                project_config.data_url,
                project_config.calculate_histogram_metrics,
                project_config.samples_per_page,
                project_config.public,
            ],
        )
        db.execute(
            "INSERT INTO user_project (user_id, project_uuid, editor) "
            "VALUES (%s,%s,%s)",
            [user.id, project_config.uuid, True],
        )
        # Create table to hold project data.
        db.execute(
            sql.SQL(
                "CREATE TABLE {}(data_id TEXT NOT NULL PRIMARY KEY, data TEXT);"
            ).format(sql.Identifier(project_config.uuid))
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

        # Create table to hold information about tags and associated datapoints.
        db.execute(
            sql.SQL(
                "CREATE TABLE {}(id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY, "
                "tag_id integer NOT NULL REFERENCES tags(id) ON DELETE CASCADE "
                "ON UPDATE CASCADE, data_id text NOT NULL REFERENCES {}(data_id) "
                "ON DELETE CASCADE ON UPDATE CASCADE);"
            ).format(
                sql.Identifier(f"{project_config.uuid}_tags_datapoints"),
                sql.Identifier(project_config.uuid),
            )
        )
        db.commit()


def dataset(
    project: str,
    data_frame: pd.DataFrame,
    id_column: str,
    label_column: str,
    data_column: str,
):
    """Adds a dataset to an existing project.

    Args:
        project (str): The project the user is currently working with.
        data_frame (pd.DataFrame): The dataset to be added.
        id_column (str): The name of the column containing the instance IDs.
        label_column (str): The name of the column containing the instance labels.
        data_column (str): The name of the column containing the raw data.
    """
    with Database() as db:
        # Drop the primary table and column_map since they will be recreated.
        db.execute(sql.SQL("DROP TABLE {} CASCADE;").format(sql.Identifier(project)))
        db.execute(
            sql.SQL("DROP TABLE {} CASCADE;").format(
                sql.Identifier(project + "_column_map")
            )
        )
        db.commit()

    # Get column objects from the dataframe.
    columns: list[ZenoColumn] = []
    for col in data_frame.columns:
        if col == id_column or col == label_column or col == data_column:
            continue
        columns.append(
            ZenoColumn(
                id=str(uuid.uuid4()),
                name=col,
                column_type=ZenoColumnType.FEATURE,
                data_type=resolve_metadata_type(data_frame, col),
            )
        )

    # Create a renaming scheme for the DataFrame columns
    column_rename = {
        id_column: "data_id",
        label_column: "label",
        data_column: "data",
    }
    for col in columns:
        column_rename[col.name] = col.id
    data_frame = data_frame.rename(columns=column_rename)
    data_frame = data_frame.set_index("data_id")

    # Add the data_id and label columns to the ones to be added to the column_map.
    columns.append(
        ZenoColumn(
            id="data_id",
            name="data_id",
            column_type=ZenoColumnType.DATA,
            data_type=MetadataType.NOMINAL,
        )
    )
    columns.append(
        ZenoColumn(
            id="label",
            name="label",
            column_type=ZenoColumnType.LABEL,
            data_type=MetadataType.NOMINAL,
        )
    )

    # Connect to the db engine using SQLAlchemy and write the data to a table.
    config = db.config()
    engine = create_engine(
        f"postgresql+psycopg://{config['user']}:{config['password']}@{config['host']}/{config['dbname']}"
    )
    data_frame.to_sql(project, con=engine, if_exists="replace", index=True)

    # Add columns to column_map
    with Database() as db:
        db.execute(
            sql.SQL(
                "CREATE TABLE {}(column_id TEXT NOT NULL PRIMARY KEY, "
                "name TEXT NOT NULL, type TEXT NOT NULL, model TEXT, "
                "data_type TEXT NOT NULL);"
            ).format(sql.Identifier(f"{project}_column_map"))
        )
        for column in columns:
            db.execute(
                sql.SQL(
                    "INSERT INTO {} (column_id, name, type, data_type) "
                    "VALUES (%s,%s,%s,%s);"
                ).format(sql.Identifier(f"{project}_column_map")),
                [column.id, column.name, column.column_type, column.data_type],
            )
        db.commit()


def system(
    project: str,
    data_frame: pd.DataFrame,
    system_name: str,
    output_column: str,
    id_column: str,
):
    """Adds a system to an existing project.

    Args:
        project (str): The project the user is currently working with.
        data_frame (pd.DataFrame): The system data to be added.
        system_name (str): The name of the system that produced the output.
        output_column (str): The name of the column containing the system output.
        id_column (str): The name of the column containing the instance IDs.
    """
    # Get column objects from the dataframe.
    output_col_object: ZenoColumn = ZenoColumn(
        id=str(uuid.uuid4()),
        name="output",
        column_type=ZenoColumnType.OUTPUT,
        data_type=MetadataType.NOMINAL,
        model=system_name,
    )
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
    config = db.config()
    engine = create_engine(
        f"postgresql+psycopg://{config['user']}:{config['password']}@{config['host']}/{config['dbname']}"
    )
    data_frame.to_sql("tmp", con=engine, if_exists="replace", index=True)
    columns.append(output_col_object)

    with Database() as db:
        for col in columns:
            db.execute(
                sql.SQL("ALTER TABLE {} ADD {}" + str(col.data_type) + ";").format(
                    sql.Identifier(project), sql.Identifier(col.id)
                )
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
    with Database() as db:
        id = db.execute_return(
            "INSERT INTO tags (name, folder_id, project_uuid) VALUES (%s,%s,%s) "
            "RETURNING id;",
            [tag.tag_name, tag.folder_id, project],
        )
        if id is None:
            return
        for datapoint in tag.data_ids:
            db.execute(
                sql.SQL("INSERT INTO {} (tag_id, data_id) VALUES (%s,%s);").format(
                    sql.Identifier(f"{project}_tags_datapoints")
                ),
                [id[0], datapoint],
            )
        db.commit()


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
