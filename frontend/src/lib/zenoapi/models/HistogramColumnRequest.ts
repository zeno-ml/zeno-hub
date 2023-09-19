/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { HistogramBucket } from './HistogramBucket';
import type { ZenoColumn } from './ZenoColumn';

/**
 * Specification of a histogram column request in Zeno.
 *
 * Attributes:
 * column (ZenoColumn): the column to be used for the histogram.
 * buckets (list[HistogramBucket]): the buckets to be used for the histogram.
 */
export type HistogramColumnRequest = {
	column: ZenoColumn;
	buckets: Array<HistogramBucket>;
};
