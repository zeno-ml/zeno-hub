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
import type { ChartResponse } from '../models/ChartResponse';
import type { Folder } from '../models/Folder';
import type { GroupMetric } from '../models/GroupMetric';
import type { HistogramBucket } from '../models/HistogramBucket';
import type { HistogramRequest } from '../models/HistogramRequest';
import type { HomepageData } from '../models/HomepageData';
import type { Metric } from '../models/Metric';
import type { MetricRequest } from '../models/MetricRequest';
import type { Organization } from '../models/Organization';
import type { Project } from '../models/Project';
import type { ProjectCopy } from '../models/ProjectCopy';
import type { ProjectsRequest } from '../models/ProjectsRequest';
import type { ProjectState } from '../models/ProjectState';
import type { Report } from '../models/Report';
import type { ReportElement } from '../models/ReportElement';
import type { ReportResponse } from '../models/ReportResponse';
import type { ReportsRequest } from '../models/ReportsRequest';
import type { Slice } from '../models/Slice';
import type { SliceElementOptions } from '../models/SliceElementOptions';
import type { SliceElementSpec } from '../models/SliceElementSpec';
import type { SliceFinderRequest } from '../models/SliceFinderRequest';
import type { SliceFinderReturn } from '../models/SliceFinderReturn';
import type { SliceTableRequest } from '../models/SliceTableRequest';
import type { StringFilterRequest } from '../models/StringFilterRequest';
import type { TableRequest } from '../models/TableRequest';
import type { Tag } from '../models/Tag';
import type { TagMetricKey } from '../models/TagMetricKey';
import type { User } from '../models/User';
import type { ZenoColumn } from '../models/ZenoColumn';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class ZenoService {
	constructor(public readonly httpRequest: BaseHttpRequest) {}

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
	 * Get Users
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
	 * Get Organization Names
	 * @returns Organization Successful Response
	 * @throws ApiError
	 */
	public getOrganizationNames(): CancelablePromise<Array<Organization>> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/organization-names'
		});
	}

	/**
	 * Get Models
	 * @param project
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public getModels(project: string): CancelablePromise<Array<string>> {
		return this.httpRequest.request({
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
	public getMetrics(project: string): CancelablePromise<Array<Metric>> {
		return this.httpRequest.request({
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
	 * Get Slices
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
	 * Get Charts
	 * @param ownerName
	 * @param projectName
	 * @returns Chart Successful Response
	 * @throws ApiError
	 */
	public getCharts(ownerName: string, projectName: string): CancelablePromise<Array<Chart>> {
		return this.httpRequest.request({
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
	 * Get Tags
	 * @param project
	 * @returns Tag Successful Response
	 * @throws ApiError
	 */
	public getTags(project: string): CancelablePromise<Array<Tag>> {
		return this.httpRequest.request({
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
	public getMetricForTag(
		project: string,
		requestBody: TagMetricKey
	): CancelablePromise<GroupMetric> {
		return this.httpRequest.request({
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
	 * Get Filtered Table
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
	 * Get Slice Element Options
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
	 * Get Slice Table
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
	 * Get Chart
	 * @param chartId
	 * @param ownerName
	 * @param projectName
	 * @returns ChartResponse Successful Response
	 * @throws ApiError
	 */
	public getChart(
		chartId: number,
		ownerName: string,
		projectName: string
	): CancelablePromise<ChartResponse> {
		return this.httpRequest.request({
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
	public getChartData(projectUuid: string, chartId: number): CancelablePromise<string> {
		return this.httpRequest.request({
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
	public getOrganizations(): CancelablePromise<Array<Organization>> {
		return this.httpRequest.request({
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
	 * @param ownerName
	 * @param projectName
	 * @returns ProjectState Successful Response
	 * @throws ApiError
	 */
	public getProjectState(ownerName: string, projectName: string): CancelablePromise<ProjectState> {
		return this.httpRequest.request({
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
	 * Get Report
	 * @param ownerName
	 * @param reportName
	 * @returns ReportResponse Successful Response
	 * @throws ApiError
	 */
	public getReport(ownerName: string, reportName: string): CancelablePromise<ReportResponse> {
		return this.httpRequest.request({
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
	public getReportElements(reportId: any): CancelablePromise<Array<ReportElement>> {
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
	 * Get Project Uuid
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
	 * @param requestBody
	 * @returns Project Successful Response
	 * @throws ApiError
	 */
	public getProjects(requestBody: ProjectsRequest): CancelablePromise<Array<Project>> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/projects',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Reports
	 * @param requestBody
	 * @returns Report Successful Response
	 * @throws ApiError
	 */
	public getReports(requestBody: ReportsRequest): CancelablePromise<Array<Report>> {
		return this.httpRequest.request({
			method: 'POST',
			url: '/reports',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Public Homepage Data
	 * @returns HomepageData Successful Response
	 * @throws ApiError
	 */
	public getPublicHomepageData(): CancelablePromise<HomepageData> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/homepage/'
		});
	}

	/**
	 * Get Homepage Data
	 * @param user
	 * @returns HomepageData Successful Response
	 * @throws ApiError
	 */
	public getHomepageData(user: string): CancelablePromise<HomepageData> {
		return this.httpRequest.request({
			method: 'GET',
			url: '/homepage/{user}',
			path: {
				user: user
			},
			errors: {
				422: `Validation Error`
			}
		});
	}

	/**
	 * Like Report
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
	 * Like Project
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
	 * Get Charts For Projects
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
	 * Get Slices For Projects
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
	 * Get Metrics For Slices
	 * @param project
	 * @param requestBody
	 * @returns GroupMetric Successful Response
	 * @throws ApiError
	 */
	public getMetricsForSlices(
		project: string,
		requestBody: MetricRequest
	): CancelablePromise<Array<GroupMetric>> {
		return this.httpRequest.request({
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
	 * Calculate Histograms
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
	 * Get Project Users
	 * @param project
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public getProjectUsers(project: string): CancelablePromise<Array<User>> {
		return this.httpRequest.request({
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
	 * Get Report Users
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
	 * Create Api Key
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
	 * Get Project Orgs
	 * @param project
	 * @returns Organization Successful Response
	 * @throws ApiError
	 */
	public getProjectOrgs(project: string): CancelablePromise<Array<Organization>> {
		return this.httpRequest.request({
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
	 * Get Report Orgs
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
	 * Filter String Metadata
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
	 * Login
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
	 * Add Folder
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
	 * Add Slice
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
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public updateSlice(project: string, requestBody: Slice): CancelablePromise<any> {
		return this.httpRequest.request({
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
	 * Add All Slices
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
	 * Add Chart
	 * @param project
	 * @param requestBody
	 * @returns number Successful Response
	 * @throws ApiError
	 */
	public addChart(project: string, requestBody: Chart): CancelablePromise<number> {
		return this.httpRequest.request({
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
	public updateChart(project: string, requestBody: Chart): CancelablePromise<any> {
		return this.httpRequest.request({
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
	 * Delete Report Element
	 * @param id
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public deleteReportElement(id: number): CancelablePromise<any> {
		return this.httpRequest.request({
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
	public addTag(project: string, requestBody: Tag): CancelablePromise<number> {
		return this.httpRequest.request({
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
	public updateTag(project: string, requestBody: Tag): CancelablePromise<any> {
		return this.httpRequest.request({
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
	 * Add Project User
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public addProjectUser(project: string, requestBody: User): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'POST',
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
	 * Update Project User
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public updateProjectUser(project: string, requestBody: User): CancelablePromise<any> {
		return this.httpRequest.request({
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
	public deleteProjectUser(project: string, requestBody: User): CancelablePromise<any> {
		return this.httpRequest.request({
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
	 * Add Project Org
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public addProjectOrg(project: string, requestBody: Organization): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'POST',
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
	 * Update Project Org
	 * @param project
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public updateProjectOrg(project: string, requestBody: Organization): CancelablePromise<any> {
		return this.httpRequest.request({
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
	public deleteProjectOrg(project: string, requestBody: Organization): CancelablePromise<any> {
		return this.httpRequest.request({
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
	 * Add Report User
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
	 * Copy Project
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
	 * Update User
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
	 * Update Project
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
	 * Update Report Org
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
	 * Delete Project
	 * @param project
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public deleteProject(project: string): CancelablePromise<any> {
		return this.httpRequest.request({
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
	 * Delete Slice
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public deleteSlice(requestBody: Slice): CancelablePromise<any> {
		return this.httpRequest.request({
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
	public deleteChart(requestBody: Chart): CancelablePromise<any> {
		return this.httpRequest.request({
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
	 * @param deleteSlices
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public deleteFolder(requestBody: Folder, deleteSlices: boolean = false): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'DELETE',
			url: '/folder',
			query: {
				delete_slices: deleteSlices
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
	 * @param requestBody
	 * @returns any Successful Response
	 * @throws ApiError
	 */
	public deleteTag(requestBody: Tag): CancelablePromise<any> {
		return this.httpRequest.request({
			method: 'DELETE',
			url: '/tag',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}
}
