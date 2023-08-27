/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Metric } from './Metric';

/**
 * Projects with datasets & models.
 *
 * Attributes:
 * uuid (str): The UUID of the task.
 * name (str): The name of the task.
 * metrics (list[Metric]): The metrics to calculate for the task.
 * owner_name (str): The name of the user who owns the task.
 * view (str): The name of the view to use for the task.
 * data_url (Optional[str]): The base URL from which to read data instances.
 * editor (bool): Whether the current user is an editor of the project.
 * calculate_histogram_metrics (bool): Whether to calculate histogram metrics.
 * Default True.
 * samples_per_page (int): The number of datapoints to show per page. Default 10.
 * public (bool): Whether the task is public. Default False.
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
