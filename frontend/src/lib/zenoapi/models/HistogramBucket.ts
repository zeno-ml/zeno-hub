/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Specification of a histogram bucket in Zeno.
 *
 * Attributes:
 * bucket (float | bool | int | str): the bucket value.
 * bucket_end (float | bool | int | str | None): the bucket end value.
 * size (int | None): the size of the bucket.
 * filtered_size (int | None): the size of the bucket after filtering.
 * metric (float | None): the metric value of the bucket.
 */
export type HistogramBucket = {
	bucket: number | boolean | string | null;
	bucketEnd?: number | boolean | string | null;
	size?: number | null;
	filteredSize?: number | null;
	metric?: number | null;
};
