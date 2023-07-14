/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Slice } from './Slice';

/**
 * Specification of the return type of a slice finder request.
 */
export type SliceFinderReturn = {
	slices: Array<Slice>;
	metrics: Array<number>;
	sizes: Array<number>;
	overallMetric?: number;
};
