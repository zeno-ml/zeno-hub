/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Join } from './Join';
import type { Operation } from './Operation';
import type { ZenoColumn } from './ZenoColumn';

/**
 * Predicates to specify a filter operation on a column of the data table.
 */
export type FilterPredicate = {
	column: ZenoColumn;
	operation: Operation;
	value: string | number | boolean;
	join: Join;
};
