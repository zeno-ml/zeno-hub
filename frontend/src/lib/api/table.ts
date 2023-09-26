import type { FilterPredicateGroup, ZenoColumn } from '$lib/zenoapi';
import { ZenoService } from '$lib/zenoapi';
import { ZenoColumnType } from '$lib/zenoapi/models/ZenoColumnType';

export async function getFilteredTable(
	project_uuid: string,
	completeColumns: ZenoColumn[],
	filterModels: string[],
	diffColumn: ZenoColumn | undefined,
	offset: number,
	limit: number,
	sort: [ZenoColumn | undefined, boolean],
	dataIds: string[],
	filterPredicates?: FilterPredicateGroup
) {
	const requestedColumns = completeColumns.filter(
		(c) =>
			c.columnType !== ZenoColumnType.EMBEDDING &&
			c.model !== undefined &&
			c.model !== null &&
			(filterModels.includes(c.model) || c.model === '')
	);

	// create diff columns for comparison view
	const diffColumn1 = diffColumn;
	let diffColumn2 = undefined;
	if (filterModels.length > 1 && diffColumn !== undefined) {
		diffColumn2 = completeColumns.find(
			(c) => c.name === diffColumn.name && c.model === filterModels[1]
		);
	}

	const res = await ZenoService.getFilteredTable(project_uuid, {
		columns: requestedColumns,
		model: filterModels[0],
		diffColumn1,
		diffColumn2,
		filterPredicates,
		offset,
		limit,
		sort,
		dataIds
	});
	return JSON.parse(res);
}
