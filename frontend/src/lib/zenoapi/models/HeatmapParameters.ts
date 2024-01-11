/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { SlicesOrModels } from './SlicesOrModels';
/**
 * Parameter specirication for a heatmap chart.
 *
 * Attributes:
 * metric (int): metric to be used in the chart.
 * x_values (list[int | str]): x values to be used in the chart.
 * y_values (list[int | str]): y values to be used in the chart.
 * model (str): model to be used in the chart.
 * y_channel (SlicesOrModels): type of the y channel.
 * x_channel (SlicesOrModels): type of the x channel.
 */
export type HeatmapParameters = {
	metric: number;
	xValues: Array<number | string>;
	yValues: Array<number | string>;
	model: string;
	yChannel: SlicesOrModels;
	xChannel: SlicesOrModels;
};
