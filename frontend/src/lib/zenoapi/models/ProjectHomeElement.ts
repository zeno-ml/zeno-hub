/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ProjectHomeElementType } from './ProjectHomeElementType';

/**
 * Representation of an element on a project's home in Zeno.
 *
 * Attributes:
 * id (int): ID of the project home element.
 * type (ReportElementType): what type of element this represents.
 * data (str | None): any data that the element holds.
 * x (int): x position of the element.
 * y (int): y position of the element.
 * width (int): width of the element.
 * height (int): height of the element.
 */
export type ProjectHomeElement = {
	id?: number | null;
	type: ProjectHomeElementType;
	data?: string | null;
	x: number;
	y: number;
	width: number;
	height: number;
};
