/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SlicesOrModels } from './SlicesOrModels';

/**
 * Parameter specification for the x and color channels of a chart.
 *
 * Attributes:
 * slices (list[int]): slices to be used in the chart.
 * metric (int): metric to be used in the chart.
 * models (list[str]): models to be used in the chart.
 * color_channel (SlicesOrModels): type of the color channel.
 * x_channel (SlicesOrModels): type of the x channel.
 */
export type XCParameters = {
	slices: Array<number>;
	metric: number;
	models: Array<string>;
	colorChannel: SlicesOrModels;
	xChannel: SlicesOrModels;
};
