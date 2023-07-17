"""Functions to update data in the database."""
import json

from psycopg import DatabaseError, sql

from zeno_backend.classes.chart import Chart, ParametersEncoder
from zeno_backend.classes.filter import PredicatesEncoder
from zeno_backend.classes.folder import Folder
from zeno_backend.classes.slice import Slice
from zeno_backend.classes.tag import Tag
from zeno_backend.database.database import Database


def folder(folder: Folder, project: str):
    """Update data for a specified folder.

    Args:
        folder (Folder): the folder data to use for the update.
        project (str): the project the user is currently working with.
    """
    db = Database()
    db.connect_execute(
        "UPDATE folders SET name = %s, project_uuid = %s WHERE id = %s;",
        [folder.name, project, folder.id],
    )


def slice(slice: Slice, project: str):
    """Update data for a specified slice.

    Args:
        slice (Slice): the slice data to use for the update.
        project (str): the project the user is currently working with.
    """
    db = Database()
    db.connect_execute(
        "UPDATE slices SET project_uuid = %s, name = %s, folder_id = %s, filter = %s "
        "WHERE id = %s;",
        [
            project,
            slice.slice_name,
            slice.folder_id,
            json.dumps(slice.filter_predicates, cls=PredicatesEncoder),
            slice.id,
        ],
    )


def chart(chart: Chart, project: str):
    """Update data for a specified chart.

    Args:
        chart (Chart): the chart data to use for the update.
        project (str): the project the user is currently working with.
    """
    db = Database()
    db.connect_execute(
        "UPDATE charts SET project_uuid = %s, name = %s, type = %s, parameters = %s "
        "WHERE id = %s;",
        [
            project,
            chart.name,
            chart.type,
            json.dumps(chart.parameters, cls=ParametersEncoder),
            chart.id,
        ],
    )


def tag(tag: Tag, project: str):
    """Update data for a specified tag.

    Args:
        tag (Tag): the tag data to use for the update.
        project (str): the project the user is currently working with.
    """
    db = Database()
    print(tag)
    try:
        db.connect()
        db.execute(
            "UPDATE tags SET project_uuid = %s, name = %s, folder_id = %s "
            "WHERE id = %s;",
            [
                project,
                tag.tag_name,
                tag.folder_id,
                tag.id,
            ],
        )
        item_ids_result = db.execute_return(
            sql.SQL("SELECT item_id FROM {} WHERE tag_id = %s;").format(
                sql.Identifier(f"{project}_tags_items")
            ),
            [
                tag.id,
            ],
            return_all=True,
        )
        print(item_ids_result)
        if item_ids_result is None:
            return
        existing_items = set(map(lambda item_id: item_id[0], item_ids_result))
        new_items = set(tag.items)
        to_remove = list(existing_items.difference(new_items))
        for item in to_remove:
            db.execute(
                sql.SQL("DELETE FROM {} WHERE tag_id = %s AND item_id = %s;").format(
                    sql.Identifier(f"{project}_tags_items")
                ),
                [
                    tag.id,
                    item,
                ],
            )
        to_add = list(new_items.difference(existing_items))
        for item in to_add:
            db.execute(
                sql.SQL("INSERT INTO {} (tag_id, item_id) VALUES (%s,%s);").format(
                    sql.Identifier(f"{project}_tags_items")
                ),
                [tag.id, item],
            )
        db.commit()
    except (Exception, DatabaseError) as error:
        raise Exception(error) from error
    finally:
        db.disconnect()
