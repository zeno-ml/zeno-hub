"""Functions to delete data from the database."""
from psycopg import sql

from zeno_backend.classes.user import Author, Organization, User
from zeno_backend.database.database import db_pool


async def project(project: str):
    """Deletes a project with a specific id.

    Args:
        project (str): the id of the project to be deleted.

    Raises:
        Exception: something went wrong while deleting the project from the database.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            # Drop the primary table with project data.
            await cur.execute(
                sql.SQL("DROP TABLE IF EXISTS {} CASCADE;").format(
                    sql.Identifier(project)
                )
            )
            # Drop the table with column properties.
            await cur.execute(
                sql.SQL("DROP TABLE IF EXISTS {} CASCADE;").format(
                    sql.Identifier(f"{project}_column_map")
                )
            )
            # Drop the table with tag data.
            await cur.execute(
                sql.SQL("DROP TABLE IF EXISTS {} CASCADE;").format(
                    sql.Identifier(f"{project}_tags_datapoints")
                )
            )
            # Delete the project from the projects table.
            await cur.execute(
                "DELETE FROM projects WHERE uuid = %s;",
                [
                    project,
                ],
            )
            await conn.commit()


async def report(report_id: int):
    """Deletes a report from Zeno.

    Args:
        report_id (int): the id of the report to be deleted.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "DELETE FROM reports WHERE id = %s;",
                [report_id],
            )
            await conn.commit()


async def folder(folder_id: int, delete_slices: bool):
    """Deletes a folder from an existing project.

    Args:
        folder_id (int): the id of the folder to be deleted.
        delete_slices (bool): whether to delete the slices in the folder as well.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            if delete_slices:
                await cur.execute(
                    "DELETE FROM slices WHERE folder_id = %s;",
                    [
                        folder_id,
                    ],
                )
            await cur.execute(
                "DELETE FROM folders WHERE id = %s;",
                [
                    folder_id,
                ],
            )
            await conn.commit()


async def slice(slice_id: int):
    """Deletes a slice from an existing project.

    Args:
        slice_id (int): the id of the slice to be deleted.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "DELETE FROM slices WHERE id = %s;",
                [slice_id],
            )
            await conn.commit()


async def chart(chart_id: int):
    """Deletes a chart from an existing project.

    Args:
        chart_id (int): the id of the chart to be deleted.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "DELETE FROM charts WHERE id = %s;",
                [
                    chart_id,
                ],
            )
            await conn.commit()


async def tag(tag_id: int):
    """Deletes a tag from an existing project.

    Args:
        tag_id (int): the id of the tag to be deleted.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "DELETE FROM tags WHERE id = %s;",
                [
                    tag_id,
                ],
            )
            await conn.commit()


async def organization(organization: Organization):
    """Deletes an organization from the database.

    Args:
        organization (Organization): the organization to delete.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "DELETE FROM organizations WHERE id = %s;",
                [
                    organization.id,
                ],
            )
            await conn.commit()


async def project_user(project: str, user: User):
    """Remove a user from a project.

    Args:
        project (str): the project id from which to remove the user.
        user (User): the user to remove.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "DELETE FROM user_project WHERE user_id = %s AND project_uuid = %s;",
                [user.id, project],
            )
            await conn.commit()


async def project_org(project: str, organization: Organization):
    """Remove an organization from a project.

    Args:
        project (str): the project id from which to remove the organization.
        organization (Organization): the organization to remove.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "DELETE FROM organization_project WHERE organization_id = %s "
                "AND project_uuid = %s;",
                [organization.id, project],
            )
            await conn.commit()


async def report_element(id: int):
    """Delete an element of a report.

    Args:
        id (int): ID of the element to be deleted.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "DELETE FROM report_elements WHERE id = %s;",
                [id],
            )
            await conn.commit()


async def report_author(report_id: int, author: Author):
    """Remove an author from a report.

    Args:
        report_id (int): the report id from which to remove the author.
        author (Author): the author to remove.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "DELETE FROM report_author WHERE user_id = %s AND report_id = %s;",
                [author.user.id, report_id],
            )
            await conn.commit()


async def report_user(report_id: int, user: User):
    """Remove a user from a report.

    Args:
        report_id (int): the report id from which to remove the user.
        user (User): the user to remove.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "DELETE FROM user_report WHERE user_id = %s AND report_id = %s;",
                [user.id, report_id],
            )
            await conn.commit()


async def report_org(report_id: int, organization: Organization):
    """Remove an organization from a report.

    Args:
        report_id (int): the report id from which to remove the organization.
        organization (Organization): the organization to remove.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "DELETE FROM organization_report WHERE organization_id = %s "
                "AND report_id = %s;",
                [organization.id, report_id],
            )
            await conn.commit()


async def dataset(project_uuid: str):
    """Delete dataset table and clear column_map for a project.

    Args:
        project_uuid (str): id of the project to delete a dataset from.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                sql.SQL("DELETE FROM {};").format(
                    sql.Identifier(f"{project_uuid}_column_map")
                )
            )
            await cur.execute(
                sql.SQL("DROP TABLE IF EXISTS {} CASCADE;").format(
                    sql.Identifier(project_uuid)
                )
            )
            await cur.execute(
                sql.SQL("DROP TABLE IF EXISTS {} CASCADE;").format(
                    sql.Identifier(f"{project_uuid}_tags_datapoints")
                )
            )
            await cur.execute(
                "UPDATE charts SET data = NULL WHERE project_uuid = %s;", [project_uuid]
            )
            await conn.commit()


async def system(project_uuid: str, system_name: str):
    """Delete a system from a project.

    Args:
        project_uuid (str): id of the project to delete a system from.
        system_name (str): name of the system to be deleted.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                sql.SQL("SELECT column_id FROM {} WHERE model = %s;").format(
                    sql.Identifier(f"{project_uuid}_column_map")
                ),
                [system_name],
            )
            columns = await cur.fetchall()
            for column in columns:
                await cur.execute(
                    sql.SQL("ALTER TABLE {} DROP COLUMN IF EXISTS {};").format(
                        sql.Identifier(project_uuid),
                        sql.Identifier(column[0]),
                    )
                )
                await cur.execute(
                    sql.SQL("DELETE FROM {} WHERE column_id = %s;").format(
                        sql.Identifier(f"{project_uuid}_column_map")
                    ),
                    [column[0]],
                )
            await cur.execute(
                "UPDATE charts SET data = NULL WHERE project_uuid = %s;", [project_uuid]
            )
            await conn.commit()


async def systems(project_uuid: str):
    """Delete all systems from a project.

    Args:
        project_uuid (str): id of the project to delete all systems from.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                sql.SQL("SELECT column_id FROM {} WHERE model IS NOT NULL;").format(
                    sql.Identifier(f"{project_uuid}_column_map")
                )
            )
            columns = await cur.fetchall()
            for column in columns:
                await cur.execute(
                    sql.SQL("ALTER TABLE {} DROP COLUMN IF EXISTS {};").format(
                        sql.Identifier(project_uuid),
                        sql.Identifier(column[0]),
                    )
                )
                await cur.execute(
                    sql.SQL("DELETE FROM {} WHERE column_id = %s;").format(
                        sql.Identifier(f"{project_uuid}_column_map")
                    ),
                    [column[0]],
                )
            await conn.commit()


async def chart_config(project_uuid: str, chart_id: int | None = None):
    """Delete the chart config for a given project or chart.

    Args:
        project_uuid (str): uuid of the project to delete the chart config for.
        chart_id (int | None): the id of the chart this is linked to. Defaults to None.
    """
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            if chart_id is None:
                await cur.execute(
                    "DELETE FROM chart_config WHERE project_uuid = %s "
                    "AND chart_id IS NULL;",
                    [project_uuid],
                )
            else:
                await cur.execute(
                    "DELETE FROM chart_config WHERE chart_id = %s;",
                    [chart_id],
                )
            await conn.commit()
