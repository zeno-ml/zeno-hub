/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { BeeswarmParameters } from './BeeswarmParameters';
import type { ChartType } from './ChartType';
import type { HeatmapParameters } from './HeatmapParameters';
import type { RadarParameters } from './RadarParameters';
import type { TableParameters } from './TableParameters';
import type { XCParameters } from './XCParameters';

/**
 * Generic chart specification with parameters for specific chart types.
 */
export type Chart = {
	id: number;
	name: string;
	type: ChartType;
	parameters:
		| XCParameters
		| TableParameters
		| BeeswarmParameters
		| RadarParameters
		| HeatmapParameters;
};
