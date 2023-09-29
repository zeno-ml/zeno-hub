"""Functions to delete data from the database."""
from psycopg import sql

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
    with Database() as db:
        # Drop the primary table with project data.
        db.execute(sql.SQL("DROP TABLE {} CASCADE;").format(sql.Identifier(project)))
        # Drop the table with column properties.
        db.execute(
            sql.SQL("DROP TABLE {} CASCADE;").format(
                sql.Identifier(f"{project}_column_map")
            )
        )
        # Drop the table with tag data.
        db.execute(
            sql.SQL("DROP TABLE {} CASCADE;").format(
                sql.Identifier(f"{project}_tags_datapoints")
            )
        )
        # Finally, delete the project from the projects table.
        db.execute(
            "DELETE FROM projects WHERE uuid = %s;",
            [
                project,
            ],
        )

        db.commit()


def report(report_id: int):
    """Deletes a report from Zeno.

    Args:
        report_id (int): the id of the report to be deleted.
    """
    db = Database()
    db.connect_execute(
        "DELETE FROM reports WHERE id = %s;",
        [
            report_id,
        ],
    )


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


def report_element(id: int):
    """Delete an element of a report.

    Args:
        id (int): ID of the element to be deleted.
    """
    db = Database()
    db.connect_execute("DELETE FROM report_elements WHERE id = %s;", [id])


def report_user(report_id: int, user: User):
    """Remove a user from a report.

    Args:
        report_id (int): the report id from which to remove the user.
        user (User): the user to remove.
    """
    db = Database()
    db.connect_execute(
        "DELETE FROM user_report WHERE user_id = %s AND report_id = %s;",
        [user.id, report_id],
    )


def report_org(report_id: int, organization: Organization):
    """Remove an organization from a report.

    Args:
        report_id (int): the report id from which to remove the organization.
        organization (Organization): the organization to remove.
    """
    db = Database()
    db.connect_execute(
        "DELETE FROM organization_report WHERE organization_id = %s "
        "AND report_id = %s;",
        [organization.id, report_id],
    )


def system(project_uuid: str, system_name: str):
    """Delete a system from a project.

    Args:
        project_uuid (str): id of the project to delete a system from.
        system_name (str): name of the system to be deleted.
    """
    with Database() as db:
        columns = db.execute_return(
            sql.SQL("SELECT column_id FROM {} WHERE model = %s;").format(
                sql.Identifier(f"{project_uuid}_column_map")
            ),
            [system_name],
        )
        for column in columns:
            db.execute(
                sql.SQL("ALTER TABLE {} DROP COLUMN {};").format(
                    sql.Identifier(project_uuid),
                    sql.Identifier(column[0]),
                )
            )
            db.execute(
                sql.SQL("DELETE FROM {} WHERE column_id = %s;").format(
                    sql.Identifier(f"{project_uuid}_column_map")
                ),
                [column[0]],
            )
        db.commit()
