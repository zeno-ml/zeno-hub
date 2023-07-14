"""Functions to delete data from the database."""
from zeno_backend.classes.chart import Chart
from zeno_backend.classes.folder import Folder
from zeno_backend.classes.slice import Slice
from zeno_backend.classes.tag import Tag
from zeno_backend.database.database import Database


def folder(folder: Folder):
    """Deletes a folder from an existing project.

    Args:
        folder (Folder): the folder to be deleted.
    """
    db = Database()
    db.connect_execute(
        "DELETE FROM folders WHERE id = %s;",
        [
            folder.id,
        ],
    )


def slice(req: Slice):
    """Deletes a slice from an existing project.

    Args:
        req (Slice): the slice to be deleted.
    """
    db = Database()
    db.connect_execute(
        "DELETE FROM slices WHERE id = %s;",
        [
            req.id,
        ],
    )


def chart(chart: Chart):
    """Deletes a chart from an existing project.

    Args:
        chart (Chart): the chart to be deleted.
    """
    db = Database()
    db.connect_execute(
        "DELETE FROM charts WHERE id = %s;",
        [
            chart.id,
        ],
    )


def tag(tag: Tag):
    """Deletes a tag from an existing project.

    Args:
        tag (Tag): the tag to be deleted.
    """
    db = Database()
    db.connect_execute(
        "DELETE FROM tags WHERE id = %s;",
        [
            tag.id,
        ],
    )
