/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Project } from './Project';
import type { ProjectStats } from './ProjectStats';

/**
 * Projects and details for homepage rendering.
 *
 * Attributes:
 * projects (list[Project]): project object with project metadata.
 * statistics (list[ProjectStats]): project statistics.
 * num_projects (int): number of projects.
 */
export type ProjectsDetails = {
	projects: Array<Project>;
	statistics: Array<ProjectStats>;
	numProjects: number;
};
