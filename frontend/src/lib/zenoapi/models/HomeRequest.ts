/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { EntrySort } from './EntrySort';
import type { EntryTypeFilter } from './EntryTypeFilter';
/**
 * Request for homepage entries.
 *
 * Attributes:
 * user_name: Username of user to get entries for. If None, get public entries.
 * project_offset: Offset of project entries already fetched
 * report_offset: Offset of report entries already fetched
 * limit: Limit of entries to return
 * search_string: String to search for in entries
 * type_filter: Type of entry to filter by
 * sort: Sort order for entries
 */
export type HomeRequest = {
	userName?: string | null;
	projectOffset?: number;
	reportOffset?: number;
	limit?: number | null;
	searchString?: string;
	typeFilter?: EntryTypeFilter;
	sort?: EntrySort;
};
