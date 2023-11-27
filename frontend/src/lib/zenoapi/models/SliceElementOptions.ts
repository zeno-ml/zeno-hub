/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Project } from './Project';

/**
 * Necessary options to render a slice report element.
 *
 * Attributes:
 * slice_name (str): name of the slice to render.
 * slice_size (int): number of instances in the slice.
 * view (str): name of the instance view.
 * id_column (str): name of the column containing the instance id.
 * data_column (str | None): name of the column containing the instance data.
 * label_column (str | None): name of the column containing the instance label.
 * system_column (str | None): name of the column containing the instance model.
 */
export type SliceElementOptions = {
	project: Project;
	sliceName: string;
	sliceSize: number;
	idColumn: string;
	dataColumn?: string | null;
	labelColumn?: string | null;
	systemColumn?: string | null;
};
