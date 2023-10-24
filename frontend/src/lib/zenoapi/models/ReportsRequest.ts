/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Request for reports in Zeno.
 *
 * Attributes:
 * offset (int): offset of the first report to get.
 * limit (int): number of reports to get.
 * order (str): order of the reports.
 */
export type ReportsRequest = {
	offset?: number;
	limit?: number | null;
	order?: string | null;
};
