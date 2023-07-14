/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { FilterPredicateGroup } from './FilterPredicateGroup';
import type { ZenoColumn } from './ZenoColumn';

/**
 * A request specification for table data.
 */
export type TableRequest = {
	columns: Array<ZenoColumn>;
	diffColumn1?: ZenoColumn;
	diffColumn2?: ZenoColumn;
	offset: number;
	limit: number;
	filterPredicates?: FilterPredicateGroup;
	sort: Array<any>;
	items?: Array<string>;
};
