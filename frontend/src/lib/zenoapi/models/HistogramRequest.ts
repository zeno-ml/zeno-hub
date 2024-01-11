/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { FilterPredicateGroup } from './FilterPredicateGroup';
import type { Metric } from './Metric';
import type { ZenoColumn } from './ZenoColumn';
/**
 * Specification of a histogram request in Zeno.
 *
 * Attributes:
 * columns (list[ZenoColumn]): the columns to calculate histograms for.
 * filter_predicates (FilterPredicateGroup | None): the filter predicates to be
 * applied to the data.
 * model (str | None): the model to be used for the histogram.
 * metric (Metric | None): the metric to be used for the histogram.
 * data_ids (list[str] | None): the data ids to be used for the histogram.
 */
export type HistogramRequest = {
	columns: Array<ZenoColumn>;
	filterPredicates?: FilterPredicateGroup | null;
	model?: string | null;
	metric?: Metric | null;
	dataIds?: Array<string> | null;
};
