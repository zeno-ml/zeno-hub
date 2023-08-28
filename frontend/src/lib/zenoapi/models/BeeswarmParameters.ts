/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SlicesOrModels } from './SlicesOrModels';

/**
 * Parameter specification for a beeswarm chart.
 */
export type BeeswarmParameters = {
	metrics: Array<string>;
	slices: Array<number>;
	models: Array<string>;
	yChannel: SlicesOrModels;
	colorChannel: SlicesOrModels;
	fixedDimension: string;
};
