/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { User } from './User';

/**
 * Representation of a organization in Zeno.
 */
export type Organization = {
	id: number;
	name: string;
	members: Array<User>;
	admin: boolean;
};
