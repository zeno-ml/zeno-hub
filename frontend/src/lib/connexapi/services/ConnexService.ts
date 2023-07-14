/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Endpoint } from '../models/Endpoint';
import type { Project } from '../models/Project';
import type { User } from '../models/User';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ConnexService {
	/**
	 * Register User
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static registerUser(requestBody: User): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/register',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Login
	 * @param requestBody
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public static login(requestBody: User): CancelablePromise<string> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/login',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Add Endpoint
	 * @param requestBody
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public static addEndpoint(requestBody: Endpoint): CancelablePromise<string> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/add_endpoint',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Endpoints
	 * @returns Endpoint Successful Response
	 * @throws ApiError
	 */
	public static getEndpoints(): CancelablePromise<Array<Endpoint>> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/endpoints'
		});
	}

	/**
	 * Add Project
	 * @param requestBody
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public static addProject(requestBody: Project): CancelablePromise<string> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/add_project',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get All Projects
	 * @returns Project Successful Response
	 * @throws ApiError
	 */
	public static getAllProjects(): CancelablePromise<Array<Project>> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/all_projects'
		});
	}

	/**
	 * Get Project
	 * @param projectId
	 * @returns Project Successful Response
	 * @throws ApiError
	 */
	public static getProject(projectId: string): CancelablePromise<Project> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/project',
			query: {
				project_id: projectId
			},
			errors: {
				422: `Validation Error`
			}
		});
	}
}
