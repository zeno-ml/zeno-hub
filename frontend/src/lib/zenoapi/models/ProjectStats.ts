/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Statistics for projects.
 *
 * Attributes:
 * num_instances (int): number of data instances in the project.
 * num_charts (int): number of charts that have been created for the project.
 * num_models (int): number of models associated with the project
 * num_likes (int): number of likes the report has.
 * user_liked (bool): whether the current user has liked the report.
 */
export type ProjectStats = {
	numInstances: number;
	numCharts: number;
	numModels: number;
	numLikes: number;
	userLiked: boolean;
};
