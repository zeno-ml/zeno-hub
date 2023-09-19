/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Metric } from './Metric';

/**
 * Projects with datasets & models.
 *
 * Attributes:
 * uuid (str): UUID of the task.
 * name (str): name of the task.
 * metrics (list[Metric]): metrics to calculate for the task.
 * owner_name (str): name of the user who owns the task.
 * view (str): name of the view to use for the task.
 * data_url (Optional[str]): base URL from which to read data instances.
 * editor (bool): whether the current user is an editor of the project.
 * calculate_histogram_metrics (bool): whether to calculate histogram metrics.
 * Default True.
 * samples_per_page (int): number of datapoints to show per page. Default 10.
 * public (bool): whether the task is public. Default False.
 */
export type Project = {
	uuid: string;
	name: string;
	metrics?: Array<Metric>;
	ownerName: string;
	view: string;
	dataUrl: string | null;
	editor: boolean;
	calculateHistogramMetrics?: boolean;
	samplesPerPage?: number;
	public?: boolean;
};
