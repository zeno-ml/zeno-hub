/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { FilterPredicateGroup } from './FilterPredicateGroup';

/**
 * Specification of a slice in Zeno.
 *
 * Attributes:
 * id (int): the id of the slice.
 * slice_name (str): the name of the slice.
 * folder_id (int | None): the id of the folder the slice belongs to.
 * filter_predicates (FilterPredicateGroup): the filter predicates of the slice.
 * project_uuid (str | None): the uuid of the project the slice belongs to.
 */
export type Slice = {
	id: number;
	sliceName: string;
	filterPredicates: FilterPredicateGroup;
	folderId?: number | null;
	projectUuid?: string | null;
};
