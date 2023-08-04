/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { FilterPredicateGroup } from './FilterPredicateGroup';

/**
 * Specification of a slice in Zeno.
 */
export type Slice = {
	id: number;
	sliceName: string;
	folderId?: number | null;
	filterPredicates: FilterPredicateGroup;
};
