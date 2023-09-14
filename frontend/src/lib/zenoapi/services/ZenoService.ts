/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_add_organization } from '../models/Body_add_organization';
import type { Body_upload_dataset } from '../models/Body_upload_dataset';
import type { Body_upload_system } from '../models/Body_upload_system';
import type { Chart } from '../models/Chart';
import type { ChartResponse } from '../models/ChartResponse';
import type { Folder } from '../models/Folder';
import type { GroupMetric } from '../models/GroupMetric';
import type { HistogramBucket } from '../models/HistogramBucket';
import type { HistogramRequest } from '../models/HistogramRequest';
import type { Metric } from '../models/Metric';
import type { MetricRequest } from '../models/MetricRequest';
import type { Organization } from '../models/Organization';
import type { Project } from '../models/Project';
import type { ProjectState } from '../models/ProjectState';
import type { ProjectStats } from '../models/ProjectStats';
import type { Report } from '../models/Report';
import type { ReportElement } from '../models/ReportElement';
import type { ReportResponse } from '../models/ReportResponse';
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
	 * Create Project
	 * Create a new project.
	 *
	 * Args:
	 * project (Project): Project object.
	 * api_key (str, optional): API key.
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static createProject(requestBody: Project): CancelablePromise<any> {
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
	 * Upload Dataset
	 * Upload a dataset to a Zeno project.
	 *
	 * Args:
	 * project (str): the UUID of the project to add data to.
	 * id_column (str): the name of the column containing the instance IDs.
	 * label_column (str | None, optional): the name of the column containing the
	 * instance labels. Defaults to None.
	 * data_column (str | None, optional): the name of the column containing the
	 * raw data. Only works for small text data. Defaults to None.
	 * file (UploadFile): the dataset to upload.
	 * api_key (str, optional): API key.
	 * @param project
	 * @param formData
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static uploadDataset(
		project: string,
		formData: Body_upload_dataset
	): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/dataset/{project}',
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
	 * Upload System
	 * Upload a system to a Zeno project.
	 *
	 * Args:
	 * project (str): the UUID of the project to add data to.
	 * system_name (str): the name of the system to upload.
	 * output_column (str): the name of the column containing the system output.
	 * id_column (str): the name of the column containing the instance IDs.
	 * file (UploadFile): the dataset to upload.
	 * api_key (str, optional): API key.
	 * @param project
	 * @param formData
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static uploadSystem(
		project: string,
		formData: Body_upload_system
	): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/system/{project}',
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
			url: '/organization-names'
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
			url: '/project-stats/{project}',
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
	 * @param ownerName
	 * @param projectName
	 * @returns Chart Successful Response
	 * @throws ApiError
	 */
	public static getCharts(ownerName: string, projectName: string): CancelablePromise<Array<Chart>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/charts/{owner}/{project}',
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
	 * @param projectUuid
	 * @param requestBody
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public static getFilteredTable(
		projectUuid: string,
		requestBody: TableRequest
	): CancelablePromise<string> {
		return __request(OpenAPI, {
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
	 * Get Chart
	 * @param chartId
	 * @param ownerName
	 * @param projectName
	 * @returns ChartResponse Successful Response
	 * @throws ApiError
	 */
	public static getChart(
		chartId: number,
		ownerName: string,
		projectName: string
	): CancelablePromise<ChartResponse> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/chart/{owner}/{project}/{chart_id}',
			path: {
				chart_id: chartId
			},
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
	 * Get Chart Data
	 * @param projectUuid
	 * @param chartId
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public static getChartData(projectUuid: string, chartId: number): CancelablePromise<string> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/chart-data/{project_uuid}/{chart_id}',
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
	 * Is Project Public
	 * @param projectUuid
	 * @returns boolean Successful Response
	 * @throws ApiError
	 */
	public static isProjectPublic(projectUuid: string): CancelablePromise<boolean> {
		return __request(OpenAPI, {
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
	 * @param ownerName
	 * @param projectName
	 * @returns ProjectState Successful Response
	 * @throws ApiError
	 */
	public static getProjectState(
		ownerName: string,
		projectName: string
	): CancelablePromise<ProjectState> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/project-state/{owner}/{project}',
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
	 * Get Report
	 * @param ownerName
	 * @param reportName
	 * @returns ReportResponse Successful Response
	 * @throws ApiError
	 */
	public static getReport(
		ownerName: string,
		reportName: string
	): CancelablePromise<ReportResponse> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/report/{owner}/{report}',
			query: {
				owner_name: ownerName,
				report_name: reportName
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Report Elements
	 * @param reportId
	 * @returns ReportElement Successful Response
	 * @throws ApiError
	 */
	public static getReportElements(reportId: any): CancelablePromise<Array<ReportElement>> {
		return __request(OpenAPI, {
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
	 * Get Project Uuid
	 * @param ownerName
	 * @param projectName
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public static getProjectUuid(ownerName: string, projectName: string): CancelablePromise<string> {
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
	 * Get Public Projects
	 * @returns Project Successful Response
	 * @throws ApiError
	 */
	public static getPublicProjects(): CancelablePromise<Array<Project>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/public-projects'
		});
	}

	/**
	 * Get Reports
	 * @returns Report Successful Response
	 * @throws ApiError
	 */
	public static getReports(): CancelablePromise<Array<Report>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/reports'
		});
	}

	/**
	 * Get Public Reports
	 * @returns Report Successful Response
	 * @throws ApiError
	 */
	public static getPublicReports(): CancelablePromise<Array<Report>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/public-reports'
		});
	}

	/**
	 * Get Charts For Projects
	 * @param requestBody
	 * @returns Chart Successful Response
	 * @throws ApiError
	 */
	public static getChartsForProjects(requestBody: Array<string>): CancelablePromise<Array<Chart>> {
		return __request(OpenAPI, {
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
	 * Calculate Histograms
	 * @param project
	 * @param requestBody
	 * @returns HistogramBucket Successful Response
	 * @throws ApiError
	 */
	public static calculateHistograms(
		project: string,
		requestBody: HistogramRequest
	): CancelablePromise<Array<Array<HistogramBucket>>> {
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
	 * Get Project Users
	 * @param project
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public static getProjectUsers(project: string): CancelablePromise<Array<User>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/project-users/{project}',
			path: {
				project: project
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Create Api Key
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public static createApiKey(): CancelablePromise<string> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/api-key/'
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
			url: '/project-organizations/{project}',
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
	 * Add Folder
	 * @param project
	 * @param name
	 * @returns number Successful Response
	 * @throws ApiError
	 */
	public static addFolder(project: string, name: string): CancelablePromise<number> {
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
	 * Update Folder
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static updateFolder(project: string, requestBody: Folder): CancelablePromise<any> {
		return __request(OpenAPI, {
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
	 * Add Slice
	 * @param project
	 * @param requestBody
	 * @returns number Successful Response
	 * @throws ApiError
	 */
	public static addSlice(project: string, requestBody: Slice): CancelablePromise<number> {
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
	 * Update Slice
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static updateSlice(project: string, requestBody: Slice): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'PATCH',
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
	 * @returns number Successful Response
	 * @throws ApiError
	 */
	public static addChart(project: string, requestBody: Chart): CancelablePromise<number> {
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
	 * Update Chart
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static updateChart(project: string, requestBody: Chart): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'PATCH',
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
	 * Add Report
	 * @param name
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static addReport(name: string): CancelablePromise<any> {
		return __request(OpenAPI, {
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
	 * @param reportId
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static addReportElement(
		reportId: number,
		requestBody: ReportElement
	): CancelablePromise<any> {
		return __request(OpenAPI, {
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
	 * Delete Report Element
	 * @param id
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static deleteReportElement(id: number): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/report-element/{id}',
			path: {
				id: id
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Add Tag
	 * @param project
	 * @param requestBody
	 * @returns number Successful Response
	 * @throws ApiError
	 */
	public static addTag(project: string, requestBody: Tag): CancelablePromise<number> {
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
	 * Update Tag
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static updateTag(project: string, requestBody: Tag): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'PATCH',
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
			url: '/add-organization',
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
			url: '/add-project-user/{project}',
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
			url: '/add-project-org/{project}',
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
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static updateOrganization(requestBody: Organization): CancelablePromise<any> {
		return __request(OpenAPI, {
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
	 * Update Project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static updateProject(requestBody: Project): CancelablePromise<any> {
		return __request(OpenAPI, {
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
	 * Update Project User
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static updateProjectUser(project: string, requestBody: User): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'PATCH',
			url: '/project-user/{project}',
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
	 * Delete Project User
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static deleteProjectUser(project: string, requestBody: User): CancelablePromise<any> {
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/project-user/{project}',
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
			method: 'PATCH',
			url: '/project-org/{project}',
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
			url: '/project-org/{project}',
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
	 * Update Report Element
	 * @param reportId
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static updateReportElement(
		reportId: number,
		requestBody: ReportElement
	): CancelablePromise<any> {
		return __request(OpenAPI, {
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
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static updateReport(requestBody: Report): CancelablePromise<any> {
		return __request(OpenAPI, {
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
	 * @param reportId
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static updateReportProjects(
		reportId: number,
		requestBody: Array<string>
	): CancelablePromise<any> {
		return __request(OpenAPI, {
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
	 * Delete Report
	 * @param reportId
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public static deleteReport(reportId: number): CancelablePromise<any> {
		return __request(OpenAPI, {
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
}
