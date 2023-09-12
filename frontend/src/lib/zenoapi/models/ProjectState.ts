/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Folder } from './Folder';
import type { Metric } from './Metric';
import type { Project } from './Project';
import type { Slice } from './Slice';
import type { Tag } from './Tag';
import type { ZenoColumn } from './ZenoColumn';

/**
 * State variables for a Zeno project.
 *
 * Attributes:
 * project (Project): The project object with project metadata.
 * models (list[str]): The names of the models in the project.
 * metrics (list[Metric]): The metrics to calculate for the project.
 * columns (list[ZenoColumn]): The columns in the project.
 * slices (list[Slice]): The slices in the project.
 * tags (list[Tag]): The tags in the project.
 * folders (list[Folder]): The folders in the project.
 */
export type ProjectState = {
	project: Project;
	models: Array<string>;
	metrics: Array<Metric>;
	columns: Array<ZenoColumn>;
	slices: Array<Slice>;
	tags: Array<Tag>;
	folders: Array<Folder>;
};
