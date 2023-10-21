/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Request for a list of projects.
 *
 * Attributes:
 * user (str): username of the user to get projects for.
 * offset (int): offset to query projects table.
 * limit (int): limit to query projects table.
 * order (str): order to sort query with.
 */
export type ProjectsRequest = {
	user?: string | null;
	offset?: number;
	limit?: number | null;
	order?: string | null;
};
