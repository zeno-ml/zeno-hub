/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Operation } from './Operation';
import type { ZenoColumn } from './ZenoColumn';

/**
 * Specification of a string filter request in Zeno.
 */
export type StringFilterRequest = {
	column: ZenoColumn;
	filterString: string;
	operation: Operation;
};
