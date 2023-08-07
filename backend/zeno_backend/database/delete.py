"""Functions to delete data from the database."""
from psycopg import DatabaseError, sql

from zeno_backend.classes.chart import Chart
from zeno_backend.classes.folder import Folder
from zeno_backend.classes.slice import Slice
from zeno_backend.classes.tag import Tag
from zeno_backend.classes.user import Organization, User
from zeno_backend.database.database import Database


def project(project: str):
    """Deletes a project with a specific id.

    Args:
        project (str): the id of the project to be deleted.

    Raises:
        Exception: something went wrong while deleting the project from the database.
    """
    db = Database()
    try:
        db.connect()
        db.execute(sql.SQL("DROP TABLE {} CASCADE;").format(sql.Identifier(project)))
        db.execute(
            sql.SQL("DROP TABLE {} CASCADE;").format(
                sql.Identifier(f"{project}_column_map")
            )
        )
        db.execute(
            sql.SQL("DROP TABLE {} CASCADE;").format(
                sql.Identifier(f"{project}_tags_items")
            )
        )
        db.execute(
            "DELETE FROM projects WHERE uuid = %s;",
            [
                project,
            ],
        )
        db.commit()
    except (Exception, DatabaseError) as error:
        raise Exception(error) from error
    finally:
        db.disconnect()


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


def organization(organization: Organization):
    """Deletes an organization from the database.

    Args:
        organization (Organization): the organization to delete.
    """
    db = Database()
    db.connect_execute("DELETE FROM organizations WHERE id = %s;", [organization.id])


def project_user(project: str, user: User):
    """Remove a user from a project.

    Args:
        project (str): the project id from which to remove the user.
        user (User): the user to remove.
    """
    db = Database()
    db.connect_execute(
        "DELETE FROM user_project WHERE user_id = %s AND project_uuid = %s;",
        [user.id, project],
    )


def project_org(project: str, organization: Organization):
    """Remove an organization from a project.

    Args:
        project (str): the project id from which to remove the organization.
        organization (Organization): the organization to remove.
    """
    db = Database()
    db.connect_execute(
        "DELETE FROM organization_project WHERE organization_id = %s "
        "AND project_uuid = %s;",
        [organization.id, project],
    )
