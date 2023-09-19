/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Tag } from './Tag';

/**
 * Specification of TagMetricKeys in Zeno.
 *
 * TagMetricKeys can be used to calculate metrics for specific tags.
 *
 * Attributes:
 * tag (Tag): tag to calculate metrics for.
 * model (str | None): model to calculate metrics for.
 * metric (int | None): metric to calculate.
 */
export type TagMetricKey = {
	tag: Tag;
	model?: string | null;
	metric?: number | null;
};
