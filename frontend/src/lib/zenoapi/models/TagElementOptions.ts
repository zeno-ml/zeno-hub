/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Project } from './Project';

/**
 * Necessary options to render a tag report element.
 *
 * Attributes:
 * tag_name (str): name of the tag to render.
 * tag_size (int): number of instances in the tag.
 * view (str): name of the instance view.
 * id_column (str): name of the column containing the instance id.
 * data_column (str | None): name of the column containing the instance data.
 * label_column (str | None): name of the column containing the instance label.
 * model_column (str | None): name of the column containing the instance model.
 */
export type TagElementOptions = {
	project: Project;
	tagName: string;
	tagSize: number;
	idColumn: string;
	dataColumn?: string | null;
	labelColumn?: string | null;
	modelColumn?: string | null;
};
