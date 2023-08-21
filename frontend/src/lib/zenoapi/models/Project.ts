/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Projects with datasets & models.
 *
 * Attributes:
 * uuid (str): UUID of the task.
 * name (str): name of the task.
 * view (str): name of the view to use for the task.
 * calculate_histogram_metrics (bool): whether to calculate histogram metrics.
 * samples_per_page (int): number of items to show per page.
 * public (bool): whether the task is public.
 * editor (bool): whether the current user is an editor of the project.
 *
 */
export type Project = {
	uuid: string;
	name: string;
	view: string;
	calculateHistogramMetrics?: boolean;
	samplesPerPage?: number;
	editor: boolean;
	public: boolean;
};
