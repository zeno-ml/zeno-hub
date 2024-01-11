/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Representation of a report in Zeno.
 *
 * Attributes:
 * id (int): ID of the report.
 * name (str): name of the report.
 * owner_name (str): name of the creater of the report
 * linked_projects (list[str]): all projects that can be used with the report.
 * editor (bool): whether the current user can edit the report.
 * public (bool): whether the report is publically visible.
 * description (str): description of the report. Default "".
 * created_at (str): ISO-format string time the report was created. Default "".
 * updated_at (str): ISO-format string time the report was last updated.
 * Default "".
 */
export type Report = {
	id: number;
	name: string;
	ownerName: string;
	linkedProjects: Array<string>;
	editor: boolean;
	public?: boolean;
	description?: string;
	createdAt?: string;
	updatedAt?: string;
};
