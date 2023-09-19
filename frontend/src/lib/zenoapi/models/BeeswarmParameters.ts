/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SlicesOrModels } from './SlicesOrModels';

/**
 * Parameter specification for a beeswarm chart.
 *
 * Attributes:
 * metrics (list[int]): metrics to be used in the chart.
 * slices (list[int]): slices to be used in the chart.
 * models (list[str]): models to be used in the chart.
 * y_channel (SlicesOrModels): type of the y channel.
 * color_channel (SlicesOrModels): type of the color channel.
 * fixed_dimension (str): fixed dimension of the chart.
 */
export type BeeswarmParameters = {
	metrics: Array<number>;
	slices: Array<number>;
	models: Array<string>;
	yChannel: SlicesOrModels;
	colorChannel: SlicesOrModels;
	fixedDimension: string;
};
