import {
	MetadataType,
	type FilterPredicateGroup,
	type ZenoColumn,
	type ZenoService
} from '$lib/zenoapi';

export async function getFilteredTable(
	project_uuid: string,
	completeColumns: ZenoColumn[],
	filterModels: string[],
	diffColumn: ZenoColumn | undefined,
	offset: number,
	limit: number,
	sort: [ZenoColumn | undefined, boolean],
	dataIds: string[],
	client: ZenoService,
	filterPredicates?: FilterPredicateGroup
) {
	const requestedColumns = completeColumns.filter(
		(c) =>
			c.dataType !== MetadataType.EMBEDDING &&
			c.model !== undefined &&
			c.model !== null &&
			(filterModels.includes(c.model) || c.model === '')
	);

	// create diff columns for comparison view
	let diffColumn1 = undefined;
	let diffColumn2 = undefined;
	if (filterModels.length > 1 && diffColumn !== undefined) {
		diffColumn1 = completeColumns.find(
			(c) => c.name === diffColumn.name && c.model === filterModels[0]
		);
		diffColumn2 = completeColumns.find(
			(c) => c.name === diffColumn.name && c.model === filterModels[1]
		);
	}

	const res = await client.getFilteredTable(project_uuid, {
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
