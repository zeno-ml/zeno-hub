/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { FilterPredicate } from './FilterPredicate';
import type { Join } from './Join';

/**
 * Group of filter predicates that might be joined by a Join operator.
 *
 * Attributes:
 * predicates (list[FilterPredicateGroup | FilterPredicate]): predicates to be
 * applied for the filter.
 * join (Join): join operator to be used between groups.
 */
export type FilterPredicateGroup = {
	predicates: Array<FilterPredicateGroup | FilterPredicate>;
	join: Join;
};
