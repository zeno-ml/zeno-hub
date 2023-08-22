/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_add_organization } from '../models/Body_add_organization';
import type { Body_upload_datapoint } from '../models/Body_upload_datapoint';
import type { Chart } from '../models/Chart';
import type { DataSpec } from '../models/DataSpec';
import type { FeatureSpec } from '../models/FeatureSpec';
import type { Folder } from '../models/Folder';
import type { GroupMetric } from '../models/GroupMetric';
import type { HistogramBucket } from '../models/HistogramBucket';
import type { HistogramRequest } from '../models/HistogramRequest';
import type { LabelSpec } from '../models/LabelSpec';
import type { Metric } from '../models/Metric';
import type { MetricRequest } from '../models/MetricRequest';
import type { Organization } from '../models/Organization';
import type { OutputSpec } from '../models/OutputSpec';
import type { Project } from '../models/Project';
import type { ProjectStats } from '../models/ProjectStats';
import type { Slice } from '../models/Slice';
import type { SliceFinderRequest } from '../models/SliceFinderRequest';
import type { SliceFinderReturn } from '../models/SliceFinderReturn';
import type { StringFilterRequest } from '../models/StringFilterRequest';
import type { TableRequest } from '../models/TableRequest';
import type { Tag } from '../models/Tag';
import type { TagMetricKey } from '../models/TagMetricKey';
import type { User } from '../models/User';
import type { ZenoColumn } from '../models/ZenoColumn';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ZenoService {
	/**
	 * Get Users
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public static getUsers(): CancelablePromise<Array<User>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/users'
		});
	}

	/**
	 * Get Organization Names
	 * @returns Organization Successful Response
	 * @throws ApiError
	 */
	public static getOrganizationNames(): CancelablePromise<Array<Organization>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/organization_names'
		});
	}

	/**
	 * Get Data
	 * @param project
	 * @param dataId
	 * @returns binary Successful Response
	 * @throws ApiError
	 */
	public static getData(project: string, dataId: string): CancelablePromise<Blob> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/data/{project}',
			path: {
				project: project
			},
			query: {
				data_id: dataId
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Project Stats
	 * @param project
	 * @returns ProjectStats Successful Response
	 * @throws ApiError
	 */
	public static getProjectStats(project: string): CancelablePromise<ProjectStats> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/project_stats/{project}',
			path: {
				project: project
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Models
	 * @param project
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public static getModels(project: string): CancelablePromise<Array<string>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/models/{project}',
			path: {
				project: project
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Metrics
	 * @param project
	 * @returns Metric Successful Response
	 * @throws ApiError
	 */
	public static getMetrics(project: string): CancelablePromise<Array<Metric>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/metrics/{project}',
			path: {
				project: project
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Folders
	 * @param project
	 * @returns Folder Successful Response
	 * @throws ApiError
	 */
	public static getFolders(project: string): CancelablePromise<Array<Folder>> {
		return __request(OpenAPI, {
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
	 * Get Slices
	 * @param project
	 * @returns Slice Successful Response
	 * @throws ApiError
	 */
	public static getSlices(project: string): CancelablePromise<Array<Slice>> {
		return __request(OpenAPI, {
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
	 * Get Charts
	 * @param project
	 * @returns Chart Successful Response
	 * @throws ApiError
	 */
	public static getCharts(project: string): CancelablePromise<Array<Chart>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/charts/{project}',
			path: {
				project: project
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Columns
	 * @param project
	 * @returns ZenoColumn Successful Response
	 * @throws ApiError
	 */
	public static getColumns(project: string): CancelablePromise<Array<ZenoColumn>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/columns/{project}',
			path: {
				project: project
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Tags
	 * @param project
	 * @returns Tag Successful Response
	 * @throws ApiError
	 */
	public static getTags(project: string): CancelablePromise<Array<Tag>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/tags/{project}',
			path: {
				project: project
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Metric For Tag
	 * @param project
	 * @param requestBody
	 * @returns GroupMetric Successful Response
	 * @throws ApiError
	 */
	public static getMetricForTag(
		project: string,
		requestBody: TagMetricKey
	): CancelablePromise<GroupMetric> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/tag-metric/{project}',
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
	 * Run Slice Finder
	 * @param project
	 * @param requestBody
	 * @returns SliceFinderReturn Successful Response
	 * @throws ApiError
	 */
	public static runSliceFinder(
		project: string,
		requestBody: SliceFinderRequest
	): CancelablePromise<SliceFinderReturn> {
		return __request(OpenAPI, {
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
	 * Get Filtered Table
	 * @param project
	 * @param requestBody
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public static getFilteredTable(
		project: string,
		requestBody: TableRequest
	): CancelablePromise<string> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/filtered-table/{project}',
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
	 * Get Chart Data
	 * @param project
	 * @param requestBody
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public static getChartData(project: string, requestBody: Chart): CancelablePromise<string> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/chart-data/{project}',
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
	 * Get Organizations
	 * @returns Organization Successful Response
	 * @throws ApiError
	 */
	public static getOrganizations(): CancelablePromise<Array<Organization>> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/organizations'
		});
	}

	/**
	 * Get Project
	 * @param ownerName
	 * @param projectName
	 * @returns Project Successful Response
	 * @throws ApiError
	 */
	public static getProject(ownerName: string, projectName: string): CancelablePromise<Project> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/project/{owner}/{project}',
			query: {
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
	 * @returns Project Successful Response
	 * @throws ApiError
	 */
	public static getProjects(): CancelablePromise<Array<Project>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/projects'
		});
	}

	/**
	 * Get Metrics For Slices
	 * @param project
	 * @param requestBody
	 * @returns GroupMetric Successful Response
	 * @throws ApiError
	 */
	public static getMetricsForSlices(
		project: string,
		requestBody: MetricRequest
	): CancelablePromise<Array<GroupMetric>> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/slice-metrics/{project}',
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
	 * Get Histogram Buckets
	 * @param project
	 * @param requestBody
	 * @returns HistogramBucket Successful Response
	 * @throws ApiError
	 */
	public static getHistogramBuckets(
		project: string,
		requestBody: Array<ZenoColumn>
	): CancelablePromise<Array<Array<HistogramBucket>>> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/histograms/{project}',
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
	 * Calculate Histogram Counts
	 * @param project
	 * @param requestBody
	 * @returns number Successful Response
	 * @throws ApiError
	 */
	public static calculateHistogramCounts(
		project: string,
		requestBody: HistogramRequest
	): CancelablePromise<Array<Array<number>>> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/histogram-counts/{project}',
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
	 * Calculate Histogram Metrics
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static calculateHistogramMetrics(
		project: string,
		requestBody: HistogramRequest
	): CancelablePromise<Array<Array<number | null>>> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/histogram-metrics/{project}',
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
	 * Get Project Users
	 * @param project
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public static getProjectUsers(project: string): CancelablePromise<Array<User>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/project_users/{project}',
			path: {
				project: project
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Project Orgs
	 * @param project
	 * @returns Organization Successful Response
	 * @throws ApiError
	 */
	public static getProjectOrgs(project: string): CancelablePromise<Array<Organization>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/project_organizations/{project}',
			path: {
				project: project
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Filter String Metadata
	 * @param project
	 * @param requestBody
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public static filterStringMetadata(
		project: string,
		requestBody: StringFilterRequest
	): CancelablePromise<Array<string>> {
		return __request(OpenAPI, {
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
	 * Login
	 * @param name
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public static login(name: string): CancelablePromise<User> {
		return __request(OpenAPI, {
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
	 * Add Project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static addProject(requestBody: Project): CancelablePromise<any> {
		return __request(OpenAPI, {
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
	 * Upload Datapoint
	 * @param project
	 * @param formData
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static uploadDatapoint(
		project: string,
		formData: Body_upload_datapoint
	): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/upload_datapoint/{project}',
			path: {
				project: project
			},
			formData: formData,
			mediaType: 'multipart/form-data',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Add Datapoint
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static addDatapoint(project: string, requestBody: DataSpec): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/add_datapoint/{project}',
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
	 * Add Label
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static addLabel(project: string, requestBody: LabelSpec): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/label/{project}',
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
	 * Add Output
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static addOutput(project: string, requestBody: OutputSpec): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/output/{project}',
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
	 * Add Feature
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static addFeature(project: string, requestBody: FeatureSpec): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/feature/{project}',
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
	 * Add Folder
	 * @param project
	 * @param name
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static addFolder(project: string, name: string): CancelablePromise<any> {
		return __request(OpenAPI, {
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
	 * Add Slice
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static addSlice(project: string, requestBody: Slice): CancelablePromise<any> {
		return __request(OpenAPI, {
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
	 * Add Chart
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static addChart(project: string, requestBody: Chart): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/chart/{project}',
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
	 * Add Tag
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static addTag(project: string, requestBody: Tag): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/tag/{project}',
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
	 * Add Organization
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static addOrganization(requestBody: Body_add_organization): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/add_organization',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Add Project User
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static addProjectUser(project: string, requestBody: User): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/add_project_user/{project}',
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
	 * Add Project Org
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static addProjectOrg(project: string, requestBody: Organization): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/add_project_org/{project}',
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
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static updateSlice(project: string, requestBody: Slice): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/slice/update/{project}',
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
	 * Update Chart
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static updateChart(project: string, requestBody: Chart): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/chart/update/{project}',
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
	 * Update Folder
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static updateFolder(project: string, requestBody: Folder): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/folder/update/{project}',
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
	 * Update Tag
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static updateTag(project: string, requestBody: Tag): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/tag/update/{project}',
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
	 * Update User
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static updateUser(requestBody: User): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/user/update',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Update Organization
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static updateOrganization(requestBody: Organization): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/organization/update',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Update Project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static updateProject(requestBody: Project): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/project/update',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Update Project User
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static updateProjectUser(project: string, requestBody: User): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/project_user/update/{project}',
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
	 * Update Project Org
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static updateProjectOrg(
		project: string,
		requestBody: Organization
	): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/project_org/update/{project}',
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
	 * Delete Project
	 * @param project
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static deleteProject(project: string): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/project/{project}',
			path: {
				project: project
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete Slice
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static deleteSlice(requestBody: Slice): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/slice',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete Chart
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static deleteChart(requestBody: Chart): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/chart',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete Folder
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static deleteFolder(requestBody: Folder): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/folder',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete Tag
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static deleteTag(requestBody: Tag): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/tag',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete Organization
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static deleteOrganization(requestBody: Organization): CancelablePromise<any> {
		return __request(OpenAPI, {
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
	 * Delete Project User
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static deleteProjectUser(project: string, requestBody: User): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/project_user/{project}',
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
	 * Delete Project Org
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static deleteProjectOrg(
		project: string,
		requestBody: Organization
	): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/project_org/{project}',
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
}
