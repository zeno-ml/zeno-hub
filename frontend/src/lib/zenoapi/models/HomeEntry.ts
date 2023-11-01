/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Project } from './Project';
import type { ProjectStats } from './ProjectStats';
import type { Report } from './Report';
import type { ReportStats } from './ReportStats';

/**
 * Entry for homepage.
 *
 * Attributes:
 * entry: Project or Report
 * stats: ProjectStats or ReportStats
 */
export type HomeEntry = {
	entry: Project | Report;
	stats: ProjectStats | ReportStats;
};
