/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Specification of a folder in Zeno.
 *
 * Attributes:
 * id (int): the id of the folder.
 * name (str): the name of the folder.
 * project_uuid (str | None): the uuid of the project the folder belongs to.
 */
export type Folder = {
	id: number;
	name: string;
	projectUuid?: string | null;
};
