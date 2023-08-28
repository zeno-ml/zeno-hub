/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SlicesOrModels } from './SlicesOrModels';

/**
 * Parameter specirication for a heatmap chart.
 */
export type HeatmapParameters = {
	metric: string;
	xValues: Array<number | string>;
	yValues: Array<number | string>;
	model: string;
	yChannel: SlicesOrModels;
	xChannel: SlicesOrModels;
};
