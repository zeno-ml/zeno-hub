/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { User } from './User';

/**
 * Representation of an author in Zeno.
 *
 * Attributes:
 * user (User): user that is the author.
 * position (int): position of the author in the list of authors.
 */
export type Author = {
	user: User;
	position: number;
};
