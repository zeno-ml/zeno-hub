/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { FilterPredicateGroup } from './FilterPredicateGroup';
import type { ZenoColumn } from './ZenoColumn';
/**
 * A request specification for table data.
 *
 * Attributes:
 * columns (list[ZenoColumn]): the columns to be used for the table.
 * model (str | None): the model to be used for the table.
 * diff_column_1 (ZenoColumn | None): the first diff column to be used for the
 * table.
 * diff_column_2 (ZenoColumn | None): the second diff column to be used for the
 * table.
 * offset (int): the offset to be used for the table.
 * limit (int): the limit to be used for the table.
 * filter_predicates (FilterPredicateGroup | None): the filter predicates to be
 * applied to the data.
 * sort (tuple[ZenoColumn | None, bool]): the sort to be used for the table.
 * data_ids (list[str] | None): the data ids to be used for the table.
 */
export type TableRequest = {
	columns: Array<ZenoColumn>;
	model?: string | null;
	diffColumn1?: ZenoColumn | null;
	diffColumn2?: ZenoColumn | null;
	offset: number;
	limit: number;
	filterPredicates?: FilterPredicateGroup | null;
	sort: any[];
	dataIds?: Array<string> | null;
};
