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
 *
 * Attributes:
 * id (int): the id of the chart.
 * name (str): the name of the chart.
 * type (ChartType): the type of the chart.
 * parameters (XCParameters | TableParameters | BeeswarmParameters |
 * RadarParameters | HeatmapParameters): the parameters of the chart.
 * project_uuid (str | None): the project uuid of the chart.
 */
export type Chart = {
	id: number;
	name: string;
	projectUuid: string;
	type: ChartType;
	parameters:
		| XCParameters
		| TableParameters
		| BeeswarmParameters
		| RadarParameters
		| HeatmapParameters;
};
