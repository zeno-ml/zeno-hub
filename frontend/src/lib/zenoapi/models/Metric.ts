/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Specification for a metric in a Zeno project.
 *
 * Attributes:
 * id (int): the id of the metric to be used.
 * name (str): The name of the metric.
 * type (str): The type of metric to calculate.
 * columns (list[str]): The columns to calculate the metric on.
 */
export type Metric = {
	id: number;
	name: string;
	type: string;
	columns: Array<string>;
};
