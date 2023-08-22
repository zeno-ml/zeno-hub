/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class DefaultService {
	/**
	 * Get Project Uuid
	 * @param ownerName
	 * @param projectName
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static getProjectUuid(ownerName: string, projectName: string): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/project-uuid/{owner_name}/{project_name}',
			path: {
				owner_name: ownerName,
				project_name: projectName
			},
			errors: {
				422: `Validation Error`
			}
		});
	}
}
