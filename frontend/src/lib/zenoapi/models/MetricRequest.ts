/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { MetricKey } from './MetricKey';

/**
 * Specification of a metric request in Zeno.
 *
 * Can be used to request metric calculation on specific data subsets.
 */
export type MetricRequest = {
	metricKeys: Array<MetricKey>;
	dataIds?: Array<string> | null;
};
