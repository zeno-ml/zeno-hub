/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SlicesOrModels } from './SlicesOrModels';

/**
 * Parameter specification for the x and color channels of a chart.
 */
export type XCParameters = {
	slices: Array<number>;
	metric: string;
	models: Array<string>;
	colorChannel: SlicesOrModels;
	xChannel: SlicesOrModels;
};
