/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Metric to calculate for a Zeno project.
 *
 * Attributes:
 * name (str): The name of the metric.
 * type (str): The type of metric to calculate.
 * columns (list[str]): The columns to calculate the metric on.
 */
export type Metric = {
	name: string;
	type: string;
	columns: Array<string>;
};
