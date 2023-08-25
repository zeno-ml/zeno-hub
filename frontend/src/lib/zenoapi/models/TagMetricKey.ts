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
 *
 * Attributes:
 * tag (Tag): The tag to calculate metrics for.
 * model (str | None): The model to calculate metrics for.
 * metric (Metric | None): The metric to calculate.
 */
export type TagMetricKey = {
	tag: Tag;
	model?: string | null;
	metric?: Metric | null;
};
