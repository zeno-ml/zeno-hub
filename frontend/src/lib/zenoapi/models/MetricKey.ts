/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Slice } from './Slice';
/**
 * Specification of metric keys in zeno.
 *
 * Metric keys map to a specific slice, model, and metric.
 *
 * Attributes:
 * slice (Slice): the slice to be used for the metric.
 * model (str): the model to be used for the metric.
 * metric (int): the metric to be used for the metric.
 */
export type MetricKey = {
	slice: Slice;
	model: string;
	metric: number;
};
