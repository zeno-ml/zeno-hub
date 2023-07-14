/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { HistogramBucket } from './HistogramBucket';
import type { ZenoColumn } from './ZenoColumn';

/**
 * Specification of a histogram column request in Zeno.
 */
export type HistogramColumnRequest = {
	column: ZenoColumn;
	buckets: Array<HistogramBucket>;
};
