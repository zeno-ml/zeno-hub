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
 * offset: Offset of entries to return
 * limit: Limit of entries to return
 * search_string: String to search for in entries
 * type_filter: Type of entry to filter by
 * sort: Sort order for entries
 */
export type HomeRequest = {
	userName?: string | null;
	offset?: number;
	limit?: number | null;
	searchString?: string;
	typeFilter?: EntryTypeFilter;
	sort?: EntrySort;
};
