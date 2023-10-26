/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Report } from './Report';
import type { ReportStats } from './ReportStats';

/**
 * Reports and details for homepage rendering.
 *
 * Attributes:
 * reports (list[Report]): report object with report metadata.
 * statistics (list[ReportStats]): report statistics.
 * num_reports (int): total number of reports.
 */
export type ReportsDetails = {
	reports: Array<Report>;
	statistics: Array<ReportStats>;
	numReports: number;
};
