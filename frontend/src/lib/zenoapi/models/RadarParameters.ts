/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SlicesMetricsOrModels } from './SlicesMetricsOrModels';
import type { SlicesOrModels } from './SlicesOrModels';

/**
 * Parameter specification for a radar chart.
 *
 * Attributes:
 * metrics (list[int]): metrics to be used in the chart.
 * slices (list[int]): slices to be used in the chart.
 * models (list[str]): models to be used in the chart.
 * axis_channel (SlicesMetricsOrModels): type of the axis channel.
 * layer_channel (SlicesOrModels): type of the layer channel.
 * fixed_channel (SlicesMetricsOrModels): type of the fixed channel.
 */
export type RadarParameters = {
	metrics: Array<number>;
	slices: Array<number>;
	models: Array<string>;
	axisChannel: SlicesMetricsOrModels;
	layerChannel: SlicesOrModels;
	fixedChannel: SlicesMetricsOrModels;
};
