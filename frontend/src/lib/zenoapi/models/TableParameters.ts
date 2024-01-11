/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { SlicesMetricsOrModels } from './SlicesMetricsOrModels';
import type { SlicesOrModels } from './SlicesOrModels';
/**
 * Parameter specification for a tabular visualization.
 *
 * Attributes:
 * metrics (list[int]): metrics to be used in the chart.
 * slices (list[int]): slices to be used in the chart.
 * models (list[str]): models to be used in the chart.
 * y_channel (SlicesOrModels): type of the y channel.
 * x_channel (SlicesMetricsOrModels): type of the x channel.
 * fixed_channel (SlicesMetricsOrModels): type of the fixed channel.
 */
export type TableParameters = {
	metrics: Array<number>;
	slices: Array<number>;
	models: Array<string>;
	yChannel: SlicesOrModels;
	xChannel: SlicesMetricsOrModels;
	fixedChannel: SlicesMetricsOrModels;
};
