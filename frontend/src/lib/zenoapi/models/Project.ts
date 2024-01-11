/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Metric } from './Metric';
/**
 * Projects with datasets & models.
 *
 * Attributes:
 * uuid (str): UUID of the project.
 * name (str): name of the project.
 * description (str): description of the project. Default "".
 * metrics (list[Metric]): metrics to calculate for the project.
 * owner_name (str): name of the user who owns the project.
 * view (str): name of the view to use for the project.
 * editor (bool): whether the current user is an editor of the project.
 * samples_per_page (int): number of datapoints to show per page. Default 10.
 * public (bool): whether the project is public. Default False.
 * created_at (str): ISO-format string time the project was created. Default "".
 * updated_at (str): ISO-format string time the project was last updated.
 * Default "".
 */
export type Project = {
	uuid: string;
	name: string;
	description?: string | null;
	metrics?: Array<Metric>;
	ownerName: string;
	view: string;
	editor?: boolean;
	samplesPerPage?: number | null;
	public?: boolean | null;
	createdAt?: string;
	updatedAt?: string;
};
