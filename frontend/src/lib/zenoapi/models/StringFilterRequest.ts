/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Operation } from './Operation';
import type { ZenoColumn } from './ZenoColumn';

/**
 * Specification of a string filter request in Zeno.
 *
 * Attributes:
 * column (ZenoColumn): the column to be used for the filter.
 * filter_string (str): the string to be used for the filter.
 * operation (Operation): the operation to be used for the filter.
 */
export type StringFilterRequest = {
	column: ZenoColumn;
	filterString: string;
	operation: Operation;
};
