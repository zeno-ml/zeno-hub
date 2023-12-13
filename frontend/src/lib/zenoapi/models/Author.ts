/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { User } from './User';

/**
 * Zeno report author for displaying author list.
 *
 * Attributes:
 * user (User): User object for author.
 * position (int): position of the author in the list of authors.
 */
export type Author = {
	user: User;
	position: number;
};
