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
 */
export type ReportElement = {
	id?: number | null;
	type: ReportElementType;
	position: number;
	data?: string | null;
};
