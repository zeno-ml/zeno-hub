/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Project } from './Project';
import type { Report } from './Report';

/**
 * Projects, reports, and metadata for homepage rendering.
 *
 * Attributes:
 * projects (list[Project]): the projects to be displayed.
 * reports (list[Report]): the reports to be displayed.
 * num_projects (int): the number of projects.
 * num_reports (int): the number of reports.
 */
export type HomepageData = {
	projects: Array<Project>;
	reports: Array<Report>;
	numProjects: number;
	numReports: number;
};
