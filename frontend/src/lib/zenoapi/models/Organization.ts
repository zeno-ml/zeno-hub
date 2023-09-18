/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { User } from './User';

/**
 * Representation of a organization in Zeno.
 *
 * Attributes:
 * id (int): ID of the organization.
 * name (str): name of the organization.
 * members (list[User]): members of the organization.
 * admin (bool): whether the current user is an admin of the organization.
 */
export type Organization = {
	id: number;
	name: string;
	members: Array<User>;
	admin: boolean;
};
