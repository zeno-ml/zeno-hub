/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Statistical numbers of a Zeno report.
 *
 * Attributes:
 * num_projects (int): number of projects that are linked to the report.
 * num_elements (int): number of elements in the report.
 * num_likes (int): number of likes the report has.
 * user_liked (bool): whether the current user has liked the report.
 */
export type ReportStats = {
	numProjects: number;
	numElements: number;
	numLikes: number;
	userLiked: boolean;
};
