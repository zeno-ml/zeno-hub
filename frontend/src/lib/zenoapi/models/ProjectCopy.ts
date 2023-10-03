/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Specification for copying a Zeno project.
 *
 * Attributes:
 * name (str): name of the new project.
 * data_url (str|None): base URL from which to read data instances.
 * copy_data (bool): whether to copy the data instances.
 * copy_systems (bool): whether to copy the systems.
 * copy_slices (bool): whether to copy the slices.
 * copy_charts (bool): whether to copy the charts.
 */
export type ProjectCopy = {
	name: string;
	dataUrl: string | null;
	copyData: boolean;
	copySystems: boolean;
	copySlices: boolean;
	copyCharts: boolean;
};
