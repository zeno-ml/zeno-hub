/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { FilterPredicate } from './FilterPredicate';
import type { Join } from './Join';

/**
 * Group of filter predicates that might be joined by a Join operator.
 */
export type FilterPredicateGroup = {
	predicates: Array<FilterPredicateGroup | FilterPredicate>;
	join: Join;
};
