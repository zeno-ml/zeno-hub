/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ReportElementType } from './ReportElementType';

/**
 * Representation of an element of a Zeno report.
 *
 * Attributes:
 * id (int): ID of the report element.
 * type (ReportElementType): what type of element this represents.
 * position (int): position of the element in the report.
 * data (str | None): any data that the element holds.
 */
export type ReportElement = {
	id?: number | null;
	type: ReportElementType;
	position: number;
	data?: string | null;
};
