/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { FilterPredicateGroup } from './FilterPredicateGroup';
import type { ZenoColumn } from './ZenoColumn';

/**
 * Specification of a request to the slice finder functionality.
 *
 * Attributes:
 * metric_column (ZenoColumn): the metric column to be used.
 * search_columns (list[ZenoColumn]): the search columns to be used.
 * order_by (str): the order by clause to be used.
 * alpha (float): the alpha value to be used for the slice finder.
 * max_lattice (int): the maximum lattice size to be used for the slice finder.
 * compare_column (ZenoColumn | None): the compare column to be used.
 * filter_predicates (FilterPredicateGroup | None): the filter predicates to be
 * applied to the data.
 * data_ids (list[str] | None): the data ids to be used for the slice finder.
 */
export type SliceFinderRequest = {
	metricColumn: ZenoColumn;
	searchColumns: Array<ZenoColumn>;
	orderBy: string;
	alpha: number;
	maxLattice: number;
	compareColumn?: ZenoColumn | null;
	filterPredicates?: FilterPredicateGroup | null;
	dataIds?: Array<string> | null;
};
