"""Functions to update data in the database."""
import json

from psycopg import sql

from zeno_backend.classes.chart import Chart, ParametersEncoder
from zeno_backend.classes.filter import PredicatesEncoder
from zeno_backend.classes.folder import Folder
from zeno_backend.classes.metric import Metric
from zeno_backend.classes.project import Project
from zeno_backend.classes.report import Report, ReportElement
from zeno_backend.classes.slice import Slice
from zeno_backend.classes.tag import Tag
from zeno_backend.classes.user import Author, Organization, User
from zeno_backend.database.database import db_pool
from zeno_backend.database.select import user as get_user
from zeno_backend.processing.chart import calculate_chart_data


async def folder(folder: Folder, project: str):
    """Update data for a specified folder.

    Args:
        folder (Folder): the folder data to use for the update.
        project (str): the project the user is currently working with.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE folders SET name = %s, project_uuid = %s WHERE id = %s;",
                [folder.name, project, folder.id],
            )


async def slice(slice: Slice, project: str):
    """Update data for a specified slice.

    Args:
        slice (Slice): the slice data to use for the update.
        project (str): the project the user is currently working with.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE slices SET project_uuid = %s, name = %s, folder_id = %s, "
                "filter = %s WHERE id = %s;",
                [
                    project,
                    slice.slice_name,
                    slice.folder_id,
                    json.dumps(slice.filter_predicates, cls=PredicatesEncoder),
                    slice.id,
                ],
            )


async def chart(chart: Chart, project: str):
    """Update data for a specified chart.

    Args:
        chart (Chart): the chart data to use for the update.
        project (str): the project the user is currently working with.
    """
    chart_data = await calculate_chart_data(chart, project)

    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE charts SET project_uuid = %s, name = %s, type = %s, "
                "parameters = %s, data = %s, updated_at = CURRENT_TIMESTAMP "
                "WHERE id = %s;",
                [
                    project,
                    chart.name,
                    chart.type,
                    json.dumps(chart.parameters, cls=ParametersEncoder),
                    chart_data,
                    chart.id,
                ],
            )

    return chart_data


async def chart_data(chart_id: int, data: str):
    """Add chart data to chart entry.

    Args:
        chart_id (int): the chart id.
        data (str): the chart data to use for the update.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE charts SET data = %s WHERE id = %s;",
                [
                    data,
                    chart_id,
                ],
            )


async def clear_chart_data(project_uuid: str):
    """Set chart data from all charts for a given project to NULL.

    Args:
        project_uuid (str): the id of the project to null chart data from.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE charts SET data = NULL WHERE project_uuid = %s;",
                [
                    project_uuid,
                ],
            )
            await conn.commit()


async def tag(tag: Tag, project: str):
    """Update data for a specified tag.

    Args:
        tag (Tag): the tag data to use for the update.
        project (str): the project the user is currently working with.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE tags SET project_uuid = %s, name = %s, folder_id = %s "
                "WHERE id = %s;",
                [
                    project,
                    tag.tag_name,
                    tag.folder_id,
                    tag.id,
                ],
            )
            await cur.execute(
                sql.SQL("SELECT data_id FROM {} WHERE tag_id = %s;").format(
                    sql.Identifier(f"{project}_tags_datapoints")
                ),
                [
                    tag.id,
                ],
            )
            data_ids_result = await cur.fetchall()
            if data_ids_result is None:
                return

            existing_data = set(map(lambda d: d[0], data_ids_result))
            new_data = set(tag.data_ids)
            to_remove = list(existing_data.difference(new_data))
            for data_id in to_remove:
                await cur.execute(
                    sql.SQL(
                        "DELETE FROM {} WHERE tag_id = %s AND data_id = %s;"
                    ).format(sql.Identifier(f"{project}_tags_datapoints")),
                    [
                        tag.id,
                        data_id,
                    ],
                )

            to_add = list(new_data.difference(existing_data))
            for data_id in to_add:
                await cur.execute(
                    sql.SQL("INSERT INTO {} (tag_id, data_id) VALUES (%s,%s);").format(
                        sql.Identifier(f"{project}_tags_datapoints")
                    ),
                    [tag.id, data_id],
                )
            await conn.commit()


async def user(user: User):
    """Update a user in the database.

    Args:
        user (User): the updated representation of the user.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE users SET name = %s, display_name = %s, cognito_id = %s "
                "WHERE id = %s",
                [user.name, user.display_name, user.cognito_id, user.id],
            )


async def organization(organization: Organization):
    """Update an organization in the database.

    Includes updating the organization's members.

    Args:
        organization (Organization): the updated representation of the organization.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE organizations SET name = %s WHERE id = %s",
                [organization.name, organization.id],
            )
            await cur.execute(
                "SELECT user_id, admin FROM user_organization "
                "WHERE organization_id = %s",
                [organization.id],
            )
            organization_users = await cur.fetchall()
            if organization_users is None:
                return
            org_users = set(map(lambda user: user.id, organization.members))
            existing_users = set(map(lambda user: user[0], organization_users))
            to_remove = list(existing_users.difference(org_users))
            for user in to_remove:
                await cur.execute(
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
                await cur.execute(
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
                await cur.execute(
                    "UPDATE user_organization SET admin = %s "
                    "WHERE user_id = %s AND organization_id = %s;",
                    [user.admin, user.id, organization.id],
                )
            await conn.commit()


async def project(project_config: Project):
    """Update a project's configuration.

    Args:
        project_config (Project): the configuration of the project.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE projects SET name = %s, "
                "view = %s, samples_per_page = %s, public = %s, "
                "description = %s, updated_at = CURRENT_TIMESTAMP WHERE uuid = %s;",
                [
                    project_config.name,
                    project_config.view,
                    project_config.samples_per_page,
                    project_config.public,
                    project_config.description,
                    project_config.uuid,
                ],
            )
            await conn.commit()


async def project_metrics(project_config: Project):
    """Update a project's metrics.

    Args:
        project_config (Project): the configuration of the project.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT id, name, type, columns FROM metrics WHERE project_uuid = %s;",
                [project_config.uuid],
            )
            metric_results = await cur.fetchall()
            metrics = list(
                map(
                    lambda metric: Metric(
                        id=metric[0],
                        name=metric[1],
                        type=metric[2],
                        columns=metric[3],
                    ),
                    metric_results,
                )
            )
            new_metrics = project_config.metrics

            for metric in metrics:
                # check if the metric matches one to be added
                index = next(
                    (
                        i
                        for i, new_metric in enumerate(new_metrics)
                        if new_metric.name == metric.name
                        and set(new_metric.columns) == set(metric.columns)
                        and new_metric.type == metric.type
                    ),
                    None,
                )

                # if there is no match with an existing metric, delete the metric
                if index is None:
                    await cur.execute(
                        "DELETE FROM metrics WHERE project_uuid = %s AND id = %s;",
                        [project_config.uuid, metric.id],
                    )
                    # also reset chart data since definition changed
                    await cur.execute(
                        "UPDATE charts SET data = NULL WHERE project_uuid = %s;",
                        [
                            project_config.uuid,
                        ],
                    )

                # if there is a match, we don't have to add the metric
                else:
                    new_metrics.pop(index)

            for metric in new_metrics:
                await cur.execute(
                    "INSERT INTO metrics (project_uuid, name, type, columns) VALUES "
                    "(%s, %s, %s, %s);",
                    [project_config.uuid, metric.name, metric.type, metric.columns],
                )
            await conn.commit()


async def report(report: Report):
    """Update a report's configuration.

    Args:
        report (Report): the configuration of the report.
    """
    owner_id = await get_user(report.owner_name)
    if owner_id is None:
        return
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE reports SET name = %s, owner_id = %s, public = %s, "
                "description = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s;",
                [
                    report.name,
                    owner_id.id,
                    report.public,
                    report.description,
                    report.id,
                ],
            )


async def report_projects(report_id: int, project_uuids: list):
    """Update a report's projects.

    Args:
        report_id (str): the id of the report.
        project_uuids (list): the list of project ids.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "DELETE FROM report_project WHERE report_id = %s;",
                [report_id],
            )
            for project_uuid in project_uuids:
                await cur.execute(
                    "INSERT INTO report_project (report_id, project_uuid) "
                    "VALUES (%s,%s)",
                    [report_id, project_uuid],
                )
            await conn.commit()


async def project_user(project: str, user: User):
    """Update a user's project access in the database.

    Args:
        project (str): the project for which to update the access.
        user (User): the user for which to update the access.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE user_project SET editor = %s WHERE project_uuid = %s"
                " AND user_id = %s;",
                [user.admin, project, user.id],
            )


async def project_org(project: str, organization: Organization):
    """Update a organization's project access in the database.

    Args:
        project (str): the project for which to update the access.
        organization (Organization): the organization for which to update the access.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE organization_project SET editor = %s WHERE project_uuid = %s "
                "AND organization_id = %s;",
                [organization.admin, project, organization.id],
            )


async def report_element(element: ReportElement):
    """Update an elements for a report.

    Args:
        element (ReportElement): the element to be updated.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE report_elements SET type = %s, data = %s, position = %s"
                " WHERE id = %s RETURNING report_id;",
                [
                    element.type,
                    element.data,
                    element.position,
                    element.id,
                ],
            )
            report_id = await cur.fetchall()
            await cur.execute(
                "UPDATE reports SET updated_at = CURRENT_TIMESTAMP WHERE id = %s;",
                [report_id[0][0]],
            )
            await conn.commit()


async def report_author(author: Author, report_id: int):
    """Update an author for a report.

    Args:
        author (Author): the author to be updated.
        report_id (int): the id of the report.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE report_author SET position = %s"
                " WHERE user_id = %s AND report_id = %s;",
                [author.position, author.user.id, report_id],
            )
            await conn.commit()


async def report_user(report_id: int, user: User):
    """Update a user's report access in the database.

    Args:
        report_id (int): the report for which to update the access.
        user (User): the user for which to update the access.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE user_report SET editor = %s WHERE report_id = %s"
                " AND user_id = %s;",
                [user.admin, report_id, user.id],
            )


async def report_org(report_id: int, organization: Organization):
    """Update a organization's report access in the database.

    Args:
        report_id (int): the report for which to update the access.
        organization (Organization): the organization for which to update the access.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE organization_report SET editor = %s WHERE report_id = %s "
                "AND organization_id = %s;",
                [organization.admin, report_id, organization.id],
            )
