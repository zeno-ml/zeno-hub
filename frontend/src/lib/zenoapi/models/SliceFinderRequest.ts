/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { FilterPredicateGroup } from './FilterPredicateGroup';
import type { ZenoColumn } from './ZenoColumn';

/**
 * Specification of a request to the slice finder functionality.
 */
export type SliceFinderRequest = {
	metricColumn: ZenoColumn;
	searchColumns: Array<ZenoColumn>;
	orderBy: string;
	alpha: number;
	maxLattice: number;
	compareColumn?: ZenoColumn;
	filterPredicates?: FilterPredicateGroup;
	items?: Array<string>;
};
