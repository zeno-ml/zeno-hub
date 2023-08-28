/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { FilterPredicateGroup } from './FilterPredicateGroup';
import type { HistogramColumnRequest } from './HistogramColumnRequest';

/**
 * Specification of a histogram request in Zeno.
 */
export type HistogramRequest = {
	columnRequests: Array<HistogramColumnRequest>;
	filterPredicates?: FilterPredicateGroup | null;
	model?: string | null;
	metric?: string | null;
	dataIds?: Array<string> | null;
};
