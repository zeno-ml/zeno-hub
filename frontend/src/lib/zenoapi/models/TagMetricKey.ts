/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Metric } from './Metric';
import type { Tag } from './Tag';

/**
 * Specification of TagMetricKeys in Zeno.
 *
 * TagMetricKeys can be used to calculate metrics for specific tags.
 */
export type TagMetricKey = {
	tag: Tag;
	model: string;
	metric: Metric;
};
