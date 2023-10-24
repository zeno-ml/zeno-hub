/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Project } from './Project';
import type { ProjectStats } from './ProjectStats';
import type { Report } from './Report';
import type { ReportStats } from './ReportStats';

/**
 * Projects, reports, and metadata for homepage rendering.
 *
 * Attributes:
 * projects (list[Project]): the projects to be displayed.
 * reports (list[Report]): the reports to be displayed.
 * projects_stats (list[ProjectStats]): the project stats to be displayed.
 * reports_stats (list[ReportStats]): the report stats to be displayed.
 * num_projects (int): the number of projects.
 * num_reports (int): the number of reports.
 */
export type HomepageData = {
	projects: Array<Project>;
	reports: Array<Report>;
	projectsStats: Array<ProjectStats>;
	reportsStats: Array<ReportStats>;
	numProjects: number;
	numReports: number;
};
