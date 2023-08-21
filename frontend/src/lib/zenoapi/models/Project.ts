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
 * config (TaskConfig): The configuration of the task.
 * view (str): The name of the view to use for the task.
 * data_url (str): The base URL for loading media data instances.
 * calculate_histogram_metrics (bool): Whether to calculate histogram metrics.
 * samples_per_page (int): The number of items to show per page.
 * public (bool): Whether the task is public.
 *
 */
export type Project = {
	uuid: string;
	name: string;
	view: string;
	dataUrl?: string;
	public?: boolean;
	calculateHistogramMetrics?: boolean;
	samplesPerPage?: number;
};
