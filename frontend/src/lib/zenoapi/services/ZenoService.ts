/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_add_organization } from '../models/Body_add_organization';
import type { Body_upload_dataset } from '../models/Body_upload_dataset';
import type { Body_upload_dataset_schema } from '../models/Body_upload_dataset_schema';
import type { Body_upload_system } from '../models/Body_upload_system';
import type { Body_upload_system_schema } from '../models/Body_upload_system_schema';
import type { Chart } from '../models/Chart';
import type { Folder } from '../models/Folder';
import type { GroupMetric } from '../models/GroupMetric';
import type { HistogramBucket } from '../models/HistogramBucket';
import type { HistogramRequest } from '../models/HistogramRequest';
import type { HomeEntry } from '../models/HomeEntry';
import type { HomeRequest } from '../models/HomeRequest';
import type { Metric } from '../models/Metric';
import type { MetricRequest } from '../models/MetricRequest';
import type { Organization } from '../models/Organization';
import type { Project } from '../models/Project';
import type { ProjectCopy } from '../models/ProjectCopy';
import type { ProjectState } from '../models/ProjectState';
import type { Report } from '../models/Report';
import type { ReportElement } from '../models/ReportElement';
import type { ReportResponse } from '../models/ReportResponse';
import type { Slice } from '../models/Slice';
import type { SliceElementOptions } from '../models/SliceElementOptions';
import type { SliceElementSpec } from '../models/SliceElementSpec';
import type { SliceFinderRequest } from '../models/SliceFinderRequest';
import type { SliceFinderReturn } from '../models/SliceFinderReturn';
import type { SliceTableRequest } from '../models/SliceTableRequest';
import type { StringFilterRequest } from '../models/StringFilterRequest';
import type { TableRequest } from '../models/TableRequest';
import type { Tag } from '../models/Tag';
import type { TagElementOptions } from '../models/TagElementOptions';
import type { TagElementSpec } from '../models/TagElementSpec';
import type { TagMetricKey } from '../models/TagMetricKey';
import type { TagTableRequest } from '../models/TagTableRequest';
import type { User } from '../models/User';
import type { ZenoColumn } from '../models/ZenoColumn';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class ZenoService {
	constructor(public readonly httpRequest: BaseHttpRequest) {}

	/**
	 * Login
	 * Log a user in to Zeno.
	 *
	 * Args:
	 * name (str): name of the user to be logged in.
	 * current_user (Any, optional): user making the login request.
	 * Defaults to Depends(util.auth.claim()).
	 *
	 * Raises:
	 * HTTPException: error if the login failed.
	 *
	 * Returns:
	 * User: user that has been logged in.
	 * @param name
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public login(name: string): CancelablePromise<User> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/login',
			query: {
				name: name
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Users
	 * Get all users in the database.
	 *
	 * Returns:
	 * list[User]: list of all users.
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public getUsers(): CancelablePromise<Array<User>> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/users'
		});
	}

	/**
	 * Get Organizations
	 * Get all organizations in the database.
	 *
	 * Returns:
	 * list[Organization]: list of all organizations.
	 * @returns Organization Successful Response
	 * @throws ApiError
	 */
	public getOrganizations(): CancelablePromise<Array<Organization>> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/organizations'
		});
	}

	/**
	 * Get User Organizations
	 * Get all organizations a specified user is a member of.
	 *
	 * Args:
	 * current_user (Any, optional): user making the request.
	 * Defaults to Depends(util.auth.claim()).
	 *
	 * Raises:
	 * HTTPException: error if the user is not found.
	 *
	 * Returns:
	 * list[Organization]: all organizations the user is a member of.
	 * @returns Organization Successful Response
	 * @throws ApiError
	 */
	public getUserOrganizations(): CancelablePromise<Array<Organization>> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/user_organizations'
		});
	}

	/**
	 * Create Api Key
	 * Create a new API key for a specific user.
	 *
	 * Args:
	 * current_user (Any, optional): user making the API key request.
	 * Defaults to Depends(util.auth.claim()).
	 *
	 * Returns:
	 * str | None: new API key of the user.
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public createApiKey(): CancelablePromise<string> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/api-key/'
		});
	}

	/**
	 * Add Organization
	 * Add an organization to the database.
	 *
	 * Args:
	 * user (User): user creating the new organization.
	 * organization (Organization): specification of the organization to be created.
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public addOrganization(requestBody: Body_add_organization): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/organization',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete Organization
	 * Delete an organization from the database.
	 *
	 * Args:
	 * organization (Organization): organization to be deleted.
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public deleteOrganization(requestBody: Organization): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'DELETE',
			url: '/organization',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Update User
	 * Update a user's profile.
	 *
	 * Args:
	 * user (User): updated user profile.
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public updateUser(requestBody: User): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'PATCH',
			url: '/user/',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Update Organization
	 * Update an organization in the database.
	 *
	 * Args:
	 * organization (Organization): updated organization.
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public updateOrganization(requestBody: Organization): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'PATCH',
			url: '/organization/',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Charts
	 * Get all charts of a project.
	 *
	 * Args:
	 * project_uuid (str): UUID of the project to get all charts for.
	 * request (Request): http request to get user information from.
	 *
	 * Returns:
	 * list[Chart]: list of all of a project's charts.
	 * @param projectUuid
	 * @returns Chart Successful Response
	 * @throws ApiError
	 */
	public getCharts(projectUuid: string): CancelablePromise<Array<Chart>> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/charts/{owner}/{project}',
			query: {
				project_uuid: projectUuid
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Chart
	 * Get a chart by its id.
	 *
	 * Args:
	 * project_uuid (str): UUID of the project to get a chart from.
	 * chart_id (int): id of the chart to be fetched.
	 * request (Request): http request to get user information from.
	 *
	 * Raises:
	 * HTTPException: error if the chart could not be fetched.
	 *
	 * Returns:
	 * ChartResponse: chart spec and data.
	 * @param chartId
	 * @param projectUuid
	 * @returns Chart Successful Response
	 * @throws ApiError
	 */
	public getChart(chartId: number, projectUuid: string): CancelablePromise<Chart> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/chart/{project}/{chart_id}',
			path: {
				chart_id: chartId
			},
			query: {
				project_uuid: projectUuid
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Charts For Projects
	 * Get all charts for a list of projects.
	 *
	 * Args:
	 * project_uuids (list[str]): list of UUIDs of projects to fetch all charts for.
	 * request (Request): http request to get user information from.
	 *
	 * Returns:
	 * list[Chart]: all charts for the list of projects
	 * @param requestBody
	 * @returns Chart Successful Response
	 * @throws ApiError
	 */
	public getChartsForProjects(requestBody: Array<string>): CancelablePromise<Array<Chart>> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/charts-for-projects/',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Add Chart
	 * Add a new chart to a project.
	 *
	 * Args:
	 * project_uuid (str): UUID of the project to add a chart to.
	 * chart (Chart): chart to be added to the project.
	 * request (Request): http request to get user information from.
	 * current_user (Any, optional): user making the addition of the chart.
	 * Defaults to Depends(util.auth.claim()).
	 *
	 * Raises:
	 * HTTPException: error if the chart could not be added.
	 *
	 * Returns:
	 * int: id of the newly added chart.
	 * @param projectUuid
	 * @param requestBody
	 * @returns number Successful Response
	 * @throws ApiError
	 */
	public addChart(projectUuid: string, requestBody: Chart): CancelablePromise<number> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/chart/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Update Chart
	 * Update a chart.
	 *
	 * Args:
	 * chart (Chart): new chart data.
	 * project_uuid (str): UUID of the project that holds the chart.
	 * request (Request): http request to get user information from.
	 * @param projectUuid
	 * @param requestBody
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public updateChart(projectUuid: string, requestBody: Chart): CancelablePromise<string> {
		return this.httpRequest.request({
			method: 'PATCH',
			url: '/chart/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete Chart
	 * Delete a chart from the database.
	 *
	 * Args:
	 * project_uuid (str): project to which the chart belongs.
	 * chart_id (int): id of the chart to be deleted.
	 * request (Request): http request to get user information from.
	 * @param projectUuid
	 * @param chartId
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public deleteChart(projectUuid: string, chartId: number): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'DELETE',
			url: '/chart/{project_uuid}/{chart_id}',
			path: {
				project_uuid: projectUuid,
				chart_id: chartId
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Folders
	 * Get all folders for a specific project.
	 *
	 * Args:
	 * project (str): project to get all folders for.
	 * request (Request): http request to get user information from.
	 *
	 * Returns:
	 * list[Folder]: all folders for a specific project.
	 * @param project
	 * @returns Folder Successful Response
	 * @throws ApiError
	 */
	public getFolders(project: string): CancelablePromise<Array<Folder>> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/folders/{project}',
			path: {
				project: project
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Add Folder
	 * Add a folder to a project.
	 *
	 * Args:
	 * project (str): project to add the folder to.
	 * name (str): name of the folder to be added.
	 * request (Request): http request to get user information from.
	 *
	 * Raises:
	 * HTTPException: error if folder cannot be added.
	 *
	 * Returns:
	 * int: id of the newly created folder.
	 * @param project
	 * @param name
	 * @returns number Successful Response
	 * @throws ApiError
	 */
	public addFolder(project: string, name: string): CancelablePromise<number> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/folder/{project}',
			path: {
				project: project
			},
			query: {
				name: name
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Update Folder
	 * Updatae a folder in the database.
	 *
	 * Args:
	 * folder (Folder): new folder specification.
	 * project (str): project that the folder belongs to.
	 * request (Request): http request to get user information from.
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public updateFolder(project: string, requestBody: Folder): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'PATCH',
			url: '/folder/{project}',
			path: {
				project: project
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete Folder
	 * Delete an existing folder from the database.
	 *
	 * Args:
	 * project_uuid (str): project that the folder belongs to.
	 * folder_id (int): id of the folder to be deleted.
	 * request (Request): http request to get user information from.
	 * delete_slices (bool, optional): Whether to also delete all slices in the folder.
	 * Defaults to False.
	 * @param projectUuid
	 * @param folderId
	 * @param deleteSlices
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public deleteFolder(
		projectUuid: string,
		folderId: number,
		deleteSlices: boolean = false
	): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'DELETE',
			url: '/folder/{project_uuid}/{folder_id}',
			path: {
				project_uuid: projectUuid,
				folder_id: folderId
			},
			query: {
				delete_slices: deleteSlices
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Models
	 * Get all models for a project.
	 *
	 * Args:
	 * project_uuid (str): project to get the models for.
	 * request (Request): http request to get user information from.
	 *
	 * Returns:
	 * list[str]: all models associated with a project.
	 * @param projectUuid
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public getModels(projectUuid: string): CancelablePromise<Array<string>> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/models/{project}',
			query: {
				project_uuid: projectUuid
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Columns
	 * Get all columns of a project.
	 *
	 * Args:
	 * project_uuid (str): UUID of the project to get all columns for.
	 * request (Request): http request to get user information from.
	 *
	 * Returns:
	 * list[ZenoColumn]: all columns associated with a project.
	 * @param projectUuid
	 * @returns ZenoColumn Successful Response
	 * @throws ApiError
	 */
	public getColumns(projectUuid: string): CancelablePromise<Array<ZenoColumn>> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/columns/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Home Details
	 * Get the details of the home view including projects, reports, and statistics.
	 *
	 * Args:
	 * home_request (HomeRequest): request specification for the home view.
	 * req (Request): http request to get user information from.
	 *
	 * Returns:
	 * list[HomeEntry]: list of all entries in the home view that match the request.
	 * @param requestBody
	 * @returns HomeEntry Successful Response
	 * @throws ApiError
	 */
	public getHomeDetails(requestBody: HomeRequest): CancelablePromise<Array<HomeEntry>> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/home-details',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Calculate Histograms
	 * Calculate the histograms for a project.
	 *
	 * Args:
	 * req (HistogramRequest): specification of te histogram request.
	 * project_uuid (str): UUID of the project to calculate histograms for.
	 * request (Request): http request to get user information from.
	 *
	 * Returns:
	 * list[list[HistogramBucket]]: histogram buckets for all requested histograms.
	 * @param projectUuid
	 * @param requestBody
	 * @returns HistogramBucket Successful Response
	 * @throws ApiError
	 */
	public calculateHistograms(
		projectUuid: string,
		requestBody: HistogramRequest
	): CancelablePromise<Array<Array<HistogramBucket>>> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/histograms/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Filter String Metadata
	 * Select distinct string values of a column and return their short representation.
	 *
	 * Args:
	 * project (str): the project for which to filter the column
	 * req (StringFilterRequest): the specification of the filter operation.
	 * request (Request): http request to get user information from.
	 *
	 * Returns:
	 * list[str]: the filtered string column data.
	 * @param project
	 * @param requestBody
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public filterStringMetadata(
		project: string,
		requestBody: StringFilterRequest
	): CancelablePromise<Array<string>> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/string-filter/{project}',
			path: {
				project: project
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Metrics
	 * Get all metrics for a specific project.
	 *
	 * Args:
	 * project_uuid (str): UUID of the project to fetch metrics for.
	 * request (Request): http request to get user information from.
	 *
	 * Returns:
	 * list[Metric]: all metrics associated with a specific project.
	 * @param projectUuid
	 * @returns Metric Successful Response
	 * @throws ApiError
	 */
	public getMetrics(projectUuid: string): CancelablePromise<Array<Metric>> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/metrics/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Metrics Filtered
	 * Get all metrics that match a metrics query.
	 *
	 * Args:
	 * req (MetricRequest): request specification for the metrics to be fetched.
	 * project_uuid (str): UUID of the project to fetch metrics for.
	 * request (Request): http request to get user information from.
	 *
	 * Returns:
	 * list[Metric]: metrics that match the metric request.
	 * @param projectUuid
	 * @param requestBody
	 * @returns GroupMetric Successful Response
	 * @throws ApiError
	 */
	public getMetricsFiltered(
		projectUuid: string,
		requestBody: MetricRequest
	): CancelablePromise<Array<GroupMetric>> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/slice-metrics/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Metric For Tag
	 * Get the metric for a specific tag.
	 *
	 * Args:
	 * metric_key (TagMetricKey): specification for which tag to calculate the metric.
	 * project_uuid (str): UUID of the project to calculate the metric for.
	 * request (Request): http request to get user information from.
	 *
	 * Returns:
	 * GroupMetric: the metric calculation result.
	 * @param projectUuid
	 * @param requestBody
	 * @returns GroupMetric Successful Response
	 * @throws ApiError
	 */
	public getMetricForTag(
		projectUuid: string,
		requestBody: TagMetricKey
	): CancelablePromise<GroupMetric> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/tag-metric/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Is Project Public
	 * Check if a given project is public.
	 *
	 * Args:
	 * project_uuid (str): uuid of the project to be checked.
	 * request (Request): http request to get user information from.
	 *
	 * Returns:
	 * bool: whether the specified project is public.
	 * @param projectUuid
	 * @returns boolean Successful Response
	 * @throws ApiError
	 */
	public isProjectPublic(projectUuid: string): CancelablePromise<boolean> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/project-public/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Project State
	 * Get the current state of a project.
	 *
	 * Args:
	 * project_uuid (str): uuid of the project to fetch the state for.
	 * request (Request): http request to get user information from.
	 *
	 * Raises:
	 * HTTPException: error if the state cannot be fetched.
	 *
	 * Returns:
	 * ProjectState | None: current state of the project.
	 * @param projectUuid
	 * @returns ProjectState Successful Response
	 * @throws ApiError
	 */
	public getProjectState(projectUuid: string): CancelablePromise<ProjectState> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/project-state/{uuid}',
			query: {
				project_uuid: projectUuid
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Project Uuid
	 * Get the UUID of a project by owner and project name.
	 *
	 * Args:
	 * owner_name (str): name of the project's owner.
	 * project_name (str): name of the project.
	 * request (Request): http request to get user information from.
	 *
	 * Raises:
	 * HTTPException: error if the project uuid could not be fetched.
	 *
	 * Returns:
	 * str: uuid of the requested project.
	 * @param ownerName
	 * @param projectName
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public getProjectUuid(ownerName: string, projectName: string): CancelablePromise<string> {
		return this.httpRequest.request({
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

	/**
	 * Get Projects
	 * Get all projects for the current user.
	 *
	 * Args:
	 * current_user (Any, optional): User requesting all projects.
	 * Defaults to Depends(util.auth.claim()).
	 *
	 * Returns:
	 * list[Project]: all project of the user who sent the request.
	 * @returns Project Successful Response
	 * @throws ApiError
	 */
	public getProjects(): CancelablePromise<Array<Project>> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/projects'
		});
	}

	/**
	 * Like Project
	 * Like a project.
	 *
	 * Args:
	 * project_uuid (str): UUID of the project to be liked.
	 * current_user (Any, optional): user liking the project.
	 * Defaults to Depends(util.auth.claim()).
	 * @param projectUuid
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public likeProject(projectUuid: string): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/like-project/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Project Users
	 * Get all users of a specific project.
	 *
	 * Args:
	 * project_uuid (str): UUID of the project to get all users for.
	 * request (Request): http request to get user information from.
	 *
	 * Returns:
	 * list[User]: all users who have access to the project.
	 * @param projectUuid
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public getProjectUsers(projectUuid: string): CancelablePromise<Array<User>> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/project-users/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Project Orgs
	 * Get all organizations that have access to a project.
	 *
	 * Args:
	 * project_uuid (str): UUID of the project to get all organizations for.
	 * request (Request): http request to get user information from.
	 *
	 * Returns:
	 * list[Organization]: all organizations with access to the project.
	 * @param projectUuid
	 * @returns Organization Successful Response
	 * @throws ApiError
	 */
	public getProjectOrgs(projectUuid: string): CancelablePromise<Array<Organization>> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/project-organizations/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Add Project User
	 * Add a user to a project.
	 *
	 * Args:
	 * project_uuid (str): UUID of the project to add a new user to.
	 * user (User): user to be added to the project.
	 * request (Request): http request to get user information from.
	 * @param projectUuid
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public addProjectUser(projectUuid: string, requestBody: User): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/project-user/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Update Project User
	 * Update the rights of a project user.
	 *
	 * Args:
	 * project_uuid (str): UUID of the project to update user rights for.
	 * user (User): updated user rights of a specified user.
	 * request (Request): http request to get user information from.
	 * @param projectUuid
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public updateProjectUser(projectUuid: string, requestBody: User): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'PATCH',
			url: '/project-user/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete Project User
	 * Remove a user from a project.
	 *
	 * Args:
	 * project_uuid (str): UUID of the project to remove the user from.
	 * user (User): user to be removed from the project.
	 * request (Request): http request to get user information from.
	 * @param projectUuid
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public deleteProjectUser(projectUuid: string, requestBody: User): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'DELETE',
			url: '/project-user/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Add Project Org
	 * Add an organization to a project.
	 *
	 * Args:
	 * project_uuid (str): UUID of the project to add the organizion to.
	 * organization (Organization): organization to be added to the project.
	 * request (Request): http request to get user information from.
	 * @param projectUuid
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public addProjectOrg(projectUuid: string, requestBody: Organization): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/project-org/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Update Project Org
	 * Update the rights of a project's organization.
	 *
	 * Args:
	 * project_uuid (str): UUID of the project to update organization rights for.
	 * organization (Organization): updated rights of a specified organization.
	 * request (Request): http request to get user information from.
	 * @param projectUuid
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public updateProjectOrg(projectUuid: string, requestBody: Organization): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'PATCH',
			url: '/project-org/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete Project Org
	 * Remove an organization from a project.
	 *
	 * Args:
	 * project_uuid (str): UUID of the project to remove the organization from.
	 * organization (Organization): organization to be removed from the project.
	 * request (Request): http request to get user information from.
	 * @param projectUuid
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public deleteProjectOrg(projectUuid: string, requestBody: Organization): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'DELETE',
			url: '/project-org/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Copy Project
	 * Create a copy of an existing project.
	 *
	 * Args:
	 * project_uuid (str): UUID of the project to be copied.
	 * copy_spec (ProjectCopy): specification of what content to copy over.
	 * request (Request): http request to get user information from.
	 * current_user (Any, optional): user initiating the copy request.
	 * Defaults to Depends(util.auth.claim()).
	 * @param projectUuid
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public copyProject(projectUuid: string, requestBody: ProjectCopy): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/copy-project/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Update Project
	 * Update a project's specification.
	 *
	 * Args:
	 * project (Project): updated project specification.
	 * request (Request): http request to get user information from.
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public updateProject(requestBody: Project): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'PATCH',
			url: '/project/',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete Project
	 * Delete a project from the database.
	 *
	 * Args:
	 * project_uuid (str): UUID of the project to be deleted.
	 * current_user (Any, optional): user sending the delete request.
	 * Defaults to Depends(util.auth.claim()).
	 * @param projectUuid
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public deleteProject(projectUuid: string): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'DELETE',
			url: '/project/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Report By Name
	 * Get a report by its name and owner name.
	 *
	 * Args:
	 * owner_name (str): name of the owner of the report.
	 * report_name (str): name of the report.
	 * request (Request): http request to get user information from.
	 *
	 * Raises:
	 * HTTPException: error if the report could not be loaded.
	 *
	 * Returns:
	 * Report: the requested report.
	 * @param ownerName
	 * @param reportName
	 * @returns ReportResponse Successful Response
	 * @throws ApiError
	 */
	public getReportByName(ownerName: string, reportName: string): CancelablePromise<ReportResponse> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/report-name/{owner_name}/{report_name}',
			path: {
				owner_name: ownerName,
				report_name: reportName
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Report
	 * Get a report by its id.
	 *
	 * Args:
	 * id (int): unique id of the report.
	 * request (Request): http request to get user information from.
	 *
	 * Raises:
	 * HTTPException: error if the report could not be loaded.
	 *
	 * Returns:
	 * Report: the requested report.
	 * @param id
	 * @returns ReportResponse Successful Response
	 * @throws ApiError
	 */
	public getReport(id: number): CancelablePromise<ReportResponse> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/report/{id}',
			path: {
				id: id
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Report Elements
	 * Get all elements that a report contains.
	 *
	 * Args:
	 * report_id (int): id of the report for which to fetch elements.
	 * request (Request): http request to get user information from.
	 *
	 * Returns:
	 * list[ReportElement] | None: all elements that a report contains.
	 * @param reportId
	 * @returns ReportElement Successful Response
	 * @throws ApiError
	 */
	public getReportElements(reportId: number): CancelablePromise<Array<ReportElement>> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/report-elements/{report_id}',
			path: {
				report_id: reportId
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Like Report
	 * Like a report as a user.
	 *
	 * Args:
	 * report_id (int): id of the report to be liked by the user.
	 * current_user (Any, optional): The user who wants to like the report.
	 * Defaults to Depends(util.auth.claim()).
	 * @param reportId
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public likeReport(reportId: number): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/like-report/{report_id}',
			path: {
				report_id: reportId
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Report Users
	 * Get all users  that have access to a report.
	 *
	 * Args:
	 * report_id (int): the report for which to get user access.
	 * request (Request): http request to get user information from.
	 *
	 * Returns:
	 * list[User]: the list of users who can access the report.
	 * @param reportId
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public getReportUsers(reportId: number): CancelablePromise<Array<User>> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/report-users/{report_id}',
			path: {
				report_id: reportId
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Report Orgs
	 * Get all the organizations that have access to a report.
	 *
	 * Args:
	 * report_id (int): the report for which to get organization access.
	 * request (Request): http request to get user information from.
	 *
	 * Returns:
	 * list[Organization]: the list of organizations who can access the report.
	 * @param reportId
	 * @returns Organization Successful Response
	 * @throws ApiError
	 */
	public getReportOrgs(reportId: number): CancelablePromise<Array<Organization>> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/report-organizations/{report_id}',
			path: {
				report_id: reportId
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Slice Element Options
	 * Get the options of a report's slice element.
	 *
	 * Args:
	 * slice_element_spec (SliceElementSpec): specification of the slice element.
	 * request (Request): request to get user information from.
	 *
	 * Raises:
	 * HTTPException: error if slice element options could not be loaded.
	 *
	 * Returns:
	 * SliceElementOptions | None: options of a report's slice element.
	 * @param requestBody
	 * @returns SliceElementOptions Successful Response
	 * @throws ApiError
	 */
	public getSliceElementOptions(
		requestBody: SliceElementSpec
	): CancelablePromise<SliceElementOptions> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/slice-element-options/',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Tag Element Options
	 * Get the options of a report's tag element.
	 *
	 * Args:
	 * tag_element_spec (TagElementSpec): specification of the tag element.
	 * request (Request): request to get user information from.
	 *
	 * Raises:
	 * HTTPException: error if tag element options could not be loaded.
	 *
	 * Returns:
	 * TagElementOptions | None: options of a report's tag element.
	 * @param requestBody
	 * @returns TagElementOptions Successful Response
	 * @throws ApiError
	 */
	public getTagElementOptions(requestBody: TagElementSpec): CancelablePromise<TagElementOptions> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/tag-element-options/',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Add Report
	 * Add a new report to the Database.
	 *
	 * Args:
	 * name (str): name of the report to be added.
	 * current_user (Any, optional): The user who wants to add the report.
	 * Defaults to Depends(util.auth.claim()).
	 *
	 * Raises:
	 * HTTPException: error if the report could not be added.
	 *
	 * Returns:
	 * int: id of the newly created report.
	 * @param name
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public addReport(name: string): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/report/{name}',
			path: {
				name: name
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Add Report Element
	 * Add an element to an existing report.
	 *
	 * Args:
	 * report_id (int): id of the report to add an element to.
	 * element (ReportElement): element to be added to the report.
	 * request (Request): http request to get user information from.
	 * current_user (Any, optional): user who wants to add an element to a report.
	 * Defaults to Depends(util.auth.claim()).
	 *
	 * Raises:
	 * HTTPException: error if adding an element to a report fails.
	 *
	 * Returns:
	 * id: id of the newly created report element.
	 * @param reportId
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public addReportElement(reportId: number, requestBody: ReportElement): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/report-element/{id}',
			query: {
				report_id: reportId
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Add Report User
	 * Add a user to a report.
	 *
	 * Args:
	 * report_id (int): report to add the user to.
	 * user (User): user to be added to the report.
	 * request (Request): http request to get user information from.
	 * @param reportId
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public addReportUser(reportId: number, requestBody: User): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/report-user/{report_id}',
			path: {
				report_id: reportId
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Update Report User
	 * Update a user's privileges for a report.
	 *
	 * Args:
	 * report_id (int): the report to update user privileges for.
	 * user (User): updated user privileges.
	 * request (Request): http request to get user information from.
	 * @param reportId
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public updateReportUser(reportId: number, requestBody: User): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'PATCH',
			url: '/report-user/{report_id}',
			path: {
				report_id: reportId
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete Report User
	 * Remove a user from a report.
	 *
	 * Args:
	 * report_id (int): id dof the report to remove a user from.
	 * user (User): user to be removed from the report.
	 * request (Request): http request to get user information from.
	 * @param reportId
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public deleteReportUser(reportId: number, requestBody: User): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'DELETE',
			url: '/report-user/{report_id}',
			path: {
				report_id: reportId
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Add Report Org
	 * Add an organization to a report.
	 *
	 * Args:
	 * report_id (int): report to add the user to.
	 * organization (Organization): organization to be added to the report.
	 * request (Request): http request to get user information from.
	 * @param reportId
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public addReportOrg(reportId: number, requestBody: Organization): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/report-org/{report_id}',
			path: {
				report_id: reportId
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete Report Org
	 * Remove an organizations from a report.
	 *
	 * Args:
	 * report_id (int): id dof the report to remove an organization from.
	 * organization (Organization): organization to be removed from the report.
	 * request (Request): http request to get user information from.
	 * @param reportId
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public deleteReportOrg(reportId: number, requestBody: Organization): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'DELETE',
			url: '/report-org/{report_id}',
			path: {
				report_id: reportId
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Update Report Org
	 * Update a organization's privileges for a report.
	 *
	 * Args:
	 * report_id (int): the report to update user privileges for.
	 * organization (Organization): updated organization privileges.
	 * request (Request): http request to get user information from.
	 * @param reportId
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public updateReportOrg(reportId: number, requestBody: Organization): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'PATCH',
			url: '/report-org/{project}',
			query: {
				report_id: reportId
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Update Report Element
	 * Update an element of a report.
	 *
	 * Args:
	 * report_id (int): the report to update the element for.
	 * element (ReportElement): updated report element.
	 * request (Request): http request to get user information from.
	 * @param reportId
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public updateReportElement(reportId: number, requestBody: ReportElement): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'PATCH',
			url: '/report-element/{report_id}',
			path: {
				report_id: reportId
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Update Report
	 * Update a report's settings.
	 *
	 * Args:
	 * report (Report): updated report settings.
	 * request (Request): http request to get user information from.
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public updateReport(requestBody: Report): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'PATCH',
			url: '/report/',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Update Report Projects
	 * Update the projects associated with a report.
	 *
	 * Args:
	 * report_id (int): the report to update the projects for.
	 * project_uuids (list[str]): list of project UUIDs associated with the report.
	 * request (Request): http request to get user information from.
	 * @param reportId
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public updateReportProjects(
		reportId: number,
		requestBody: Array<string>
	): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'PATCH',
			url: '/report-projects/',
			query: {
				report_id: reportId
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete Report
	 * Delete an existing report from the databse.
	 *
	 * Args:
	 * report_id (int): the id of the report to be deleted.
	 * current_user (Any, optional): The user who wants to delete the report.
	 * Defaults to Depends(util.auth.claim()).
	 *
	 * Raises:
	 * HTTPException: error if the deletion was not successful.
	 * @param reportId
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public deleteReport(reportId: number): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'DELETE',
			url: '/report/{report_id}',
			path: {
				report_id: reportId
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete Report Element
	 * Delete an element from a report.
	 *
	 * Args:
	 * report_id (int): the id of the report the element is associated with.
	 * id (int): the id of the report element to be deleted.
	 * request (Request): http request to get user information from.
	 * @param reportId
	 * @param id
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public deleteReportElement(reportId: number, id: number): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'DELETE',
			url: '/report-element/{report_id}/{id}',
			path: {
				report_id: reportId,
				id: id
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Create Project
	 * Create a new project.
	 *
	 * Args:
	 * project (Project): Project object.
	 * response (Response): response object.
	 * api_key (str, optional): API key.
	 * @param requestBody
	 * @returns Project Successful Response
	 * @throws ApiError
	 */
	public createProject(requestBody: Project): CancelablePromise<Project> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/project',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Upload Dataset Schema
	 * Upload a dataset schema to the database. Called before uploading data.
	 *
	 * Args:
	 * project_uuid (str): the UUID of the project to add data to.
	 * id_column (str): the name of the column containing the ID.
	 * data_column (str): the name of the column containing the data.
	 * label_column (str): the name of the column containing the label.
	 * file (DatasetSchema): the dataset schema to upload.
	 * api_key (str, optional): API key.
	 * @param formData
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public uploadDatasetSchema(formData: Body_upload_dataset_schema): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/dataset-schema',
			formData: formData,
			mediaType: 'multipart/form-data',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Upload Dataset
	 * Upload a dataset to a Zeno project.
	 *
	 * Args:
	 * project_uuid (str): the UUID of the project to add data to.
	 * file (UploadFile): the dataset to upload. Serialized Arrow RecordBatch.
	 * api_key (str, optional): API key.
	 * @param projectUuid
	 * @param formData
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public uploadDataset(projectUuid: string, formData: Body_upload_dataset): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/dataset/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			formData: formData,
			mediaType: 'multipart/form-data',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Upload System Schema
	 * Upload a dataset schema to the database. Called before uploading system.
	 *
	 * Args:
	 * project_uuid (str): the UUID of the project to add data to.
	 * system_name (str): the name of the system.
	 * id_column (str): the name of the column containing the ID.
	 * output_column (str): the name of the column containing the output.
	 * file (Schema): the system PyArrow schema to upload.
	 * api_key (str, optional): API key.
	 * @param formData
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public uploadSystemSchema(formData: Body_upload_system_schema): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/system-schema',
			formData: formData,
			mediaType: 'multipart/form-data',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Upload System
	 * Upload a system to a Zeno project.
	 *
	 * Args:
	 * project_uuid (str): the UUID of the project to add the system to.
	 * system_name (str): the name of the system.
	 * file (UploadFile): the system to upload. Serialized Arrow RecordBatch.
	 * api_key (str, optional): API key.
	 * @param projectUuid
	 * @param systemName
	 * @param formData
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public uploadSystem(
		projectUuid: string,
		systemName: string,
		formData: Body_upload_system
	): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/system/{project_uuid}/{system_name}',
			path: {
				project_uuid: projectUuid,
				system_name: systemName
			},
			formData: formData,
			mediaType: 'multipart/form-data',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete System
	 * Delete a system from a Zeno project.
	 *
	 * Args:
	 * project_uuid (str): the UUID of the project to delete the system from.
	 * system_name (str): the name of the system.
	 * @param projectUuid
	 * @param systemName
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public deleteSystem(projectUuid: string, systemName: string): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'DELETE',
			url: '/system/{project_uuid}/{system_name}',
			path: {
				project_uuid: projectUuid,
				system_name: systemName
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete All Systems
	 * Delete all systems from a Zeno project.
	 *
	 * Args:
	 * project_uuid (str): the UUID of the project to delete systems from.
	 * @param projectUuid
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public deleteAllSystems(projectUuid: string): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'DELETE',
			url: '/systems/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Min Client Version
	 * Get the minimum client version required to use the server.
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public minClientVersion(): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/min-client-version'
		});
	}

	/**
	 * Get Slices
	 * Fetch all slices of a project.
	 *
	 * Args:
	 * project (str): project to fetch all slices for.
	 * request (Request): http request to get user information from.
	 *
	 * Returns:
	 * list[Slice]: requested slices.
	 * @param project
	 * @returns Slice Successful Response
	 * @throws ApiError
	 */
	public getSlices(project: string): CancelablePromise<Array<Slice>> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/slices/{project}',
			path: {
				project: project
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Run Slice Finder
	 * Run slice finder to recommend slices to the user.
	 *
	 * Args:
	 * req (SliceFinderRequest): request to slice finder algorithm specifying params.
	 * project (str): project to run slice finder for.
	 * request (Request): http request to get user information from.
	 * current_user (Any, optional): user who initiated the slice finder request.
	 * Defaults to Depends(util.auth.claim()).
	 *
	 * Returns:
	 * SliceFinderReturn: the result of the slice finder algorithm.
	 * @param project
	 * @param requestBody
	 * @returns SliceFinderReturn Successful Response
	 * @throws ApiError
	 */
	public runSliceFinder(
		project: string,
		requestBody: SliceFinderRequest
	): CancelablePromise<SliceFinderReturn> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/slice-finder/{project}',
			path: {
				project: project
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Slices For Projects
	 * Get all slices for a list of projects.
	 *
	 * Args:
	 * req (list[str]): the projects to fetch slices for.
	 * request (Request): http request to get user information from.
	 *
	 * Returns:
	 * list[Slice]: all slices in all specifiec projects.
	 * @param requestBody
	 * @returns Slice Successful Response
	 * @throws ApiError
	 */
	public getSlicesForProjects(requestBody: Array<string>): CancelablePromise<Array<Slice>> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/slices-for-projects/',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Add Slice
	 * Add a slice to a project.
	 *
	 * Args:
	 * project (str): project to add the slice to.
	 * slice (Slice): slice to be added to the project.
	 * request (Request): http request to get user information from.
	 * current_user (Any, optional): User who wants to add a slice to a project.
	 * Defaults to Depends(util.auth.claim()).
	 *
	 * Raises:
	 * HTTPException: error if adding slice fails.
	 *
	 * Returns:
	 * int: id of the newly added slice.
	 * @param project
	 * @param requestBody
	 * @returns number Successful Response
	 * @throws ApiError
	 */
	public addSlice(project: string, requestBody: Slice): CancelablePromise<number> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/slice/{project}',
			path: {
				project: project
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Update Slice
	 * Update a slice in the database.
	 *
	 * Args:
	 * slice (Slice): new values of the slice to be updated.
	 * project_uuid (str): project uuid to which the slice belongs.
	 * request (Request): http request to get user information from.
	 * @param projectUuid
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public updateSlice(projectUuid: string, requestBody: Slice): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'PATCH',
			url: '/slice/{project}',
			query: {
				project_uuid: projectUuid
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Slice Instance Ids
	 * Get all instance ids of a slice.
	 *
	 * Args:
	 * slice_id (int): id of the slice to get instance ids for.
	 * model (str | None): model of the slice.
	 * id_column (ZenoColumn): column to get ids from.
	 * request (Request): http request to get user information from.
	 *
	 * Raises:
	 * HTTPException: error if the project cannot be found.
	 *
	 * Returns:
	 * list[str]: all ids of the slice.
	 * @param sliceId
	 * @param model
	 * @param requestBody
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public getSliceInstanceIds(
		sliceId: number,
		model: string | null,
		requestBody: ZenoColumn
	): CancelablePromise<Array<string>> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/slice-instance-ids/{slice_id}/{model}',
			path: {
				slice_id: sliceId,
				model: model
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Add All Slices
	 * Add all slices for a column's values.
	 *
	 * Args:
	 * project (str): project to add the slices to.
	 * column (ZenoColumn): column to add all slices for.
	 * request (Request): http request to get user information from.
	 * name (str | None, optional): name of the folder the slices should be added to.
	 * Defaults to None.
	 *
	 * Raises:
	 * HTTPException: error if adding slices fails.
	 *
	 * Returns:
	 * list[int]: ids of all added slices.
	 * @param project
	 * @param requestBody
	 * @param name
	 * @returns number Successful Response
	 * @throws ApiError
	 */
	public addAllSlices(
		project: string,
		requestBody: ZenoColumn,
		name?: string | null
	): CancelablePromise<Array<number>> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/all-slices/{project}',
			path: {
				project: project
			},
			query: {
				name: name
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete Slice
	 * Delete a slice from the database.
	 *
	 * Args:
	 * project_uuid (str): project to which the slice belongs (to check permissions).
	 * slice_id (int): id of the slice to be deleted.
	 * request (Request): http request to get user information from.
	 * @param projectUuid
	 * @param sliceId
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public deleteSlice(projectUuid: string, sliceId: number): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'DELETE',
			url: '/slice/{project_uuid}/{slice_id}',
			path: {
				project_uuid: projectUuid,
				slice_id: sliceId
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Filtered Table
	 * Get the data in a project's table.
	 *
	 * Args:
	 * req (TableRequest): specification of the data request to the table.
	 * project_uuid (str): project to fetch data for.
	 * request (Request): http request to get user information from.
	 *
	 * Returns:
	 * json: json representation of the requested data.
	 * @param projectUuid
	 * @param requestBody
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public getFilteredTable(
		projectUuid: string,
		requestBody: TableRequest
	): CancelablePromise<string> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/filtered-table/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Slice Table
	 * Get the data in a project's table for a specific slice.
	 *
	 * Args:
	 * slice_table_request (SliceTableRequest): specification of the data request.
	 * request (Request): http request to get user information from.
	 *
	 * Raises:
	 * HTTPException: error if the data cannot be loaded.
	 *
	 * Returns:
	 * json: json representation of the requested data.
	 * @param requestBody
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public getSliceTable(requestBody: SliceTableRequest): CancelablePromise<string> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/slice-table',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Tag Table
	 * Get the data in a project's table for a specific tag.
	 *
	 * Args:
	 * tag_table_request (TagTableRequest): specification of the data request.
	 * request (Request): http request to get user information from.
	 *
	 * Raises:
	 * HTTPException: errorr if the data cannot be loaded.
	 *
	 * Returns:
	 * json: json representation of the requested data.
	 * @param requestBody
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public getTagTable(requestBody: TagTableRequest): CancelablePromise<string> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/tag-table',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Tags
	 * Get all tags for a project.
	 *
	 * Args:
	 * project_uuid (str): UUID of the project to get all tags for.
	 * request (Request): http request to get user information from.
	 *
	 * Returns:
	 * list[Tag]: list of all of a project's tags.
	 * @param projectUuid
	 * @returns Tag Successful Response
	 * @throws ApiError
	 */
	public getTags(projectUuid: string): CancelablePromise<Array<Tag>> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/tags/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Tags For Projects
	 * Get all tags for a list of projects.
	 *
	 * Args:
	 * project_uuids (list[str]): UUIDs of all projects to get tags for.
	 *
	 * Returns:
	 * list[Tag]: all tags for the specified projects.
	 * @param requestBody
	 * @returns Tag Successful Response
	 * @throws ApiError
	 */
	public getTagsForProjects(requestBody: Array<string>): CancelablePromise<Array<Tag>> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/tags-for-projects/',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Add Tag
	 * Add a tag to a project.
	 *
	 * Args:
	 * tag (Tag): the tag to be added.
	 * project_uuid (str): UUID of the project to add the tag to.
	 * request (Request): http request to get user information from.
	 * current_user (Any, optional): user adding the new tag.
	 * Defaults to Depends(util.auth.claim()).
	 *
	 * Raises:
	 * HTTPException: error if adding the tag failed.
	 *
	 * Returns:
	 * int: id of the newly created tag.
	 * @param projectUuid
	 * @param requestBody
	 * @returns number Successful Response
	 * @throws ApiError
	 */
	public addTag(projectUuid: string, requestBody: Tag): CancelablePromise<number> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/tag/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Update Tag
	 * Update a tag in the database.
	 *
	 * Args:
	 * tag (Tag): updated tag.
	 * project_uuid (str): project to which the tag belongs.
	 * request (Request): http request to get user information from.
	 * @param projectUuid
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public updateTag(projectUuid: string, requestBody: Tag): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'PATCH',
			url: '/tag/{project_uuid}',
			path: {
				project_uuid: projectUuid
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete Tag
	 * Delete a tag from the database.
	 *
	 * Args:
	 * project_uuid (str): project to which the tag belongs.
	 * tag_id (int): id of the tag to be deleted.
	 * request (Request): http request to get user information from.
	 * @param projectUuid
	 * @param tagId
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public deleteTag(projectUuid: string, tagId: number): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'DELETE',
			url: '/tag/{project_uuid}/{tag_id}',
			path: {
				project_uuid: projectUuid,
				tag_id: tagId
			},
			errors: {
				422: `Validation Error`
			}
		});
	}
}
