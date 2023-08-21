/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Projects with datasets & models.
 *
 * Attributes:
 * uuid (str): The UUID of the task.
 * name (str): The name of the task.
 * view (str): The name of the view to use for the task.
 * data_url (str): The base URL from which to read data instances.
 * editor (bool): Whether the current user is an editor of the project.
 * calculate_histogram_metrics (bool): Whether to calculate histogram metrics.
 * Default True.
 * samples_per_page (int): The number of items to show per page. Default 10.
 * public (bool): Whether the task is public. Default False.
 *
 */
export type Project = {
	uuid: string;
	name: string;
	view: string;
	dataUrl: string;
	editor: boolean;
	calculateHistogramMetrics?: boolean;
	samplesPerPage?: number;
	public?: boolean;
};
