import type { FilterPredicate } from '$lib/zenoapi/models/FilterPredicate';
import type { FilterPredicateGroup } from '$lib/zenoapi/models/FilterPredicateGroup';

export function isPredicateGroup(
	element: FilterPredicateGroup | FilterPredicate
): element is FilterPredicateGroup {
	if ((element as FilterPredicateGroup).predicates !== undefined) {
		return true;
	}
	return false;
}

export function isPredicate(
	element: FilterPredicateGroup | FilterPredicate
): element is FilterPredicate {
	if ((element as FilterPredicate).column !== undefined) {
		return true;
	}
	return false;
}
