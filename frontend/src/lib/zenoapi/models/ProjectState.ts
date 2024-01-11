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
 * project (Project): project object with project metadata.
 * models (list[str]): names of the models in the project.
 * metrics (list[Metric]): metrics to calculate for the project.
 * columns (list[ZenoColumn]): columns in the project.
 * slices (list[Slice]): slices in the project.
 * tags (list[Tag]): tags in the project.
 * folders (list[Folder]): folders in the project.
 * has_data (bool): whether the project has data instances.
 * num_likes (int): number of likes the report has.
 * user_liked (bool): whether the current user has liked the report.
 */
export type ProjectState = {
	project: Project;
	models: Array<string>;
	metrics: Array<Metric>;
	columns: Array<ZenoColumn>;
	slices: Array<Slice>;
	tags: Array<Tag>;
	folders: Array<Folder>;
	hasData: boolean;
	numLikes: number;
	userLiked: boolean;
};
