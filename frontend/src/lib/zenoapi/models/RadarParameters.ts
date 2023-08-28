/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SlicesMetricsOrModels } from './SlicesMetricsOrModels';
import type { SlicesOrModels } from './SlicesOrModels';

/**
 * Parameter specification for a radar chart.
 */
export type RadarParameters = {
	metrics: Array<number>;
	slices: Array<number>;
	models: Array<string>;
	axisChannel: SlicesMetricsOrModels;
	layerChannel: SlicesOrModels;
	fixedChannel: SlicesMetricsOrModels;
};
