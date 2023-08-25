/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ReportElementType } from './ReportElementType';

/**
 * Representation of an element of a Zeno report.
 *
 * Attributes:
 * type (ReportElementType): what type of element this represents.
 * data (str | None): any data that the element holds.
 * chart_id (int | None): id of the chart this element is linked to.
 */
export type ReportElement = {
	id: number;
	type: ReportElementType;
	data: string | null;
	chartId: number | null;
	position: number;
};
