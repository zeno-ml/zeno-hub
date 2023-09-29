"""Functions to update data in the database."""
import json

from psycopg import sql

from zeno_backend.classes.chart import Chart, ParametersEncoder
from zeno_backend.classes.filter import PredicatesEncoder
from zeno_backend.classes.folder import Folder
from zeno_backend.classes.project import Project
from zeno_backend.classes.report import Report, ReportElement
from zeno_backend.classes.slice import Slice
from zeno_backend.classes.tag import Tag
from zeno_backend.classes.user import Organization, User
from zeno_backend.database.database import Database
from zeno_backend.database.select import user as get_user


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
    with Database() as db:
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
        data_ids_result = db.execute_return(
            sql.SQL("SELECT data_id FROM {} WHERE tag_id = %s;").format(
                sql.Identifier(f"{project}_tags_datapoints")
            ),
            [
                tag.id,
            ],
        )
        if data_ids_result is None:
            return

        existing_data = set(map(lambda d: d[0], data_ids_result))
        new_data = set(tag.data_ids)
        to_remove = list(existing_data.difference(new_data))
        for data_id in to_remove:
            db.execute(
                sql.SQL("DELETE FROM {} WHERE tag_id = %s AND data_id = %s;").format(
                    sql.Identifier(f"{project}_tags_datapoints")
                ),
                [
                    tag.id,
                    data_id,
                ],
            )

        to_add = list(new_data.difference(existing_data))
        for data_id in to_add:
            db.execute(
                sql.SQL("INSERT INTO {} (tag_id, data_id) VALUES (%s,%s);").format(
                    sql.Identifier(f"{project}_tags_datapoints")
                ),
                [tag.id, data_id],
            )
        db.commit()


def user(user: User):
    """Update a user in the database.

    Args:
        user (User): the updated representation of the user.
    """
    db = Database()
    db.connect_execute(
        "UPDATE users SET name = %s WHERE id = %s",
        [user.name, user.id],
    )


def organization(organization: Organization):
    """Update an organization in the database.

    Includes updating the organization's members.

    Args:
        organization (Organization): the updated representation of the organization.
    """
    with Database() as db:
        db.execute(
            "UPDATE organizations SET name = %s WHERE id = %s",
            [organization.name, organization.id],
        )
        organization_users = db.execute_return(
            "SELECT user_id, admin FROM user_organization WHERE organization_id = %s",
            [organization.id],
        )
        if organization_users is None:
            return
        org_users = set(map(lambda user: user.id, organization.members))
        existing_users = set(map(lambda user: user[0], organization_users))
        to_remove = list(existing_users.difference(org_users))
        for user in to_remove:
            db.execute(
                "DELETE FROM user_organization "
                "WHERE user_id = %s AND organization_id = %s;",
                [
                    user,
                    organization.id,
                ],
            )
        to_add = list(
            filter(lambda user: user.id not in existing_users, organization.members)
        )
        for user in to_add:
            db.execute(
                "INSERT INTO user_organization (user_id, organization_id, admin) "
                "VALUES (%s,%s,%s)",
                [user.id, organization.id, user.admin],
            )
        to_edit = list(
            filter(
                lambda user: any(
                    user.id == org_user[0] and user.admin != org_user[1]
                    for org_user in organization_users
                ),
                organization.members,
            )
        )
        for user in to_edit:
            db.execute(
                "UPDATE user_organization SET admin = %s "
                "WHERE user_id = %s AND organization_id = %s;",
                [user.admin, user.id, organization.id],
            )
        db.commit()


def project(project_config: Project):
    """Update a project's configuration.

    Args:
        project_config (Project): the configuration of the project.
    """
    with Database() as db:
        db.execute(
            "UPDATE projects SET name = %s, calculate_histogram_metrics = %s, "
            "view = %s, data_url = %s, samples_per_page = %s, public = %s, "
            "description = %s WHERE uuid = %s;",
            [
                project_config.name,
                project_config.calculate_histogram_metrics,
                project_config.view,
                project_config.data_url,
                project_config.samples_per_page,
                project_config.public,
                project_config.description,
                project_config.uuid,
            ],
        )
        db.commit()


def project_metrics(project_config: Project):
    """Update a project's metrics.

    Args:
        project_config (Project): the configuration of the project.
    """
    with Database() as db:
        db.execute(
            "DELETE FROM metrics WHERE project_uuid = %s;",
            [project_config.uuid],
        )
        for metric in project_config.metrics:
            db.execute(
                "INSERT INTO metrics (project_uuid, name, type, columns) VALUES "
                "(%s, %s, %s, %s);",
                [project_config.uuid, metric.name, metric.type, metric.columns],
            )
        db.commit()


def report(report: Report):
    """Update a report's configuration.

    Args:
        report (Report): the configuration of the report.
    """
    owner_id = get_user(report.owner_name)
    if owner_id is None:
        return
    db = Database()
    db.connect_execute(
        "UPDATE reports SET name = %s, owner_id = %s, public = %s, description = %s "
        "WHERE id = %s;",
        [report.name, owner_id.id, report.public, report.description, report.id],
    )


def report_projects(report_id: int, project_uuids: list):
    """Update a report's projects.

    Args:
        report_id (str): the id of the report.
        project_uuids (list): the list of project ids.
    """
    with Database() as db:
        db.execute(
            "DELETE FROM report_project WHERE report_id = %s;",
            [report_id],
        )
        for project_uuid in project_uuids:
            db.execute(
                "INSERT INTO report_project (report_id, project_uuid) VALUES (%s,%s);",
                [report_id, project_uuid],
            )
        db.commit()


def project_user(project: str, user: User):
    """Update a user's project access in the database.

    Args:
        project (str): the project for which to update the access.
        user (User): the user for which to update the access.
    """
    db = Database()
    db.connect_execute(
        "UPDATE user_project SET editor = %s WHERE project_uuid = %s AND user_id = %s;",
        [user.admin, project, user.id],
    )


def project_org(project: str, organization: Organization):
    """Update a organization's project access in the database.

    Args:
        project (str): the project for which to update the access.
        organization (Organization): the organization for which to update the access.
    """
    db = Database()
    db.connect_execute(
        "UPDATE organization_project SET editor = %s WHERE project_uuid = %s "
        "AND organization_id = %s;",
        [organization.admin, project, organization.id],
    )


def report_element(element: ReportElement):
    """Update an elements for a report.

    Args:
        element (ReportElement): the element to be updated.
    """
    db = Database()
    db.connect_execute(
        "UPDATE report_elements SET type = %s, data = %s, chart_id = %s, position = %s"
        " WHERE id = %s;",
        [
            element.type,
            element.data,
            element.chart_id,
            element.position,
            element.id,
        ],
    )


def report_user(report_id: int, user: User):
    """Update a user's report access in the database.

    Args:
        report_id (int): the report for which to update the access.
        user (User): the user for which to update the access.
    """
    db = Database()
    db.connect_execute(
        "UPDATE user_report SET editor = %s WHERE report_id = %s AND user_id = %s;",
        [user.admin, report_id, user.id],
    )


def report_org(report_id: int, organization: Organization):
    """Update a organization's report access in the database.

    Args:
        report_id (int): the report for which to update the access.
        organization (Organization): the organization for which to update the access.
    """
    db = Database()
    db.connect_execute(
        "UPDATE organization_report SET editor = %s WHERE report_id = %s "
        "AND organization_id = %s;",
        [organization.admin, report_id, organization.id],
    )
