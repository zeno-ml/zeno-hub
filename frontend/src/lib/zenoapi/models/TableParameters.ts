/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SlicesMetricsOrModels } from './SlicesMetricsOrModels';
import type { SlicesOrModels } from './SlicesOrModels';

/**
 * Parameter specification for a tabular visualization.
 */
export type TableParameters = {
	metrics: Array<number>;
	slices: Array<number>;
	models: Array<string>;
	yChannel: SlicesOrModels;
	xChannel: SlicesMetricsOrModels;
	fixedChannel: SlicesMetricsOrModels;
};
