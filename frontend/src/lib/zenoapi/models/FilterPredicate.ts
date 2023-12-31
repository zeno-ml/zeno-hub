/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Join } from './Join';
import type { Operation } from './Operation';
import type { ZenoColumn } from './ZenoColumn';

/**
 * Predicates to specify a filter operation on a column of the data table.
 *
 * Attributes:
 * column (ZenoColumn): column to be filtered.
 * operation (Operation): operation to be applied.
 * value (StrictStr | StrictBool | StrictInt | StrictFloat): value to filter with.
 * join (Join): join operator to be used.
 */
export type FilterPredicate = {
	column: ZenoColumn;
	operation: Operation;
	value: string | boolean | number;
	join: Join;
};
