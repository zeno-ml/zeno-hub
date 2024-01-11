/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { MetricKey } from './MetricKey';
/**
 * Specification of a metric request in Zeno.
 *
 * Can be used to request metric calculation on specific data subsets.
 *
 * Attributes:
 * metric_keys (list[MetricKey]): the metric keys to be used for the metric.
 * data_ids (list[str] | None): the data ids to be used for the metric.
 */
export type MetricRequest = {
	metricKeys: Array<MetricKey>;
	dataIds?: Array<string> | null;
};
