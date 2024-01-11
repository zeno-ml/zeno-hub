/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Slice } from './Slice';
/**
 * Specification of the return type of a slice finder request.
 *
 * Attributes:
 * slices (list[Slice]): the slices found by the slice finder.
 * metrics (list[float]): the metrics of the slices found by the slice finder.
 * sizes (list[int]): the sizes of the slices found by the slice finder.
 * overall_metric (float | None): the overall metric of the slice finder.
 */
export type SliceFinderReturn = {
	slices: Array<Slice>;
	metrics: Array<number>;
	sizes: Array<number>;
	overallMetric?: number | null;
};
