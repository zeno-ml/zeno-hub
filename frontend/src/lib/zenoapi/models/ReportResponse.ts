/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Report } from './Report';
import type { ReportElement } from './ReportElement';
/**
 * Response for a report in Zeno.
 *
 * Attributes:
 * report (Report): the report itself.
 * report_elements (list[ReportElement]): all elements of the report.
 * num_likes (int): number of likes the report has.
 * user_liked (bool): whether the current user has liked the report.
 */
export type ReportResponse = {
	report: Report;
	reportElements: Array<ReportElement>;
	numLikes: number;
	userLiked: boolean;
};
