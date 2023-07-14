/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Metric } from './Metric';
import type { Slice } from './Slice';

/**
 * Specification of metric keys in zeno.
 *
 * Metric keys map to a specific slice, model, and metric.
 */
export type MetricKey = {
	slice: Slice;
	model: string;
	metric: Metric;
};
