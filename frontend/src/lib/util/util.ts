import { env } from '$env/dynamic/public';
import { doesModelDependOnPredicates, setModelForFilterPredicateGroup } from '$lib/api/slice';
import { slicesForComparison } from '../stores';

import { Operation, ZenoColumnType, type Slice, type ZenoColumn } from '$lib/zenoapi';
import { get } from 'svelte/store';

export function getProjectRouteFromURL(url: URL) {
	let projectURL = url.origin;
	const pathParts = url.pathname.split('/');
	const projectIndex = pathParts.indexOf('project');
	for (let i = 1; i < projectIndex + 2; i++) {
		projectURL = projectURL + '/' + pathParts[i];
	}
	return projectURL;
}

export function columnHash(col: ZenoColumn) {
	return (
		(col.columnType === ZenoColumnType.METADATA ? '' : col.columnType) +
		col.name +
		(col.model ? col.model : '')
	);
}

function columnTypeOrder(colType: ZenoColumnType) {
	switch (colType) {
		case ZenoColumnType.POSTDISTILL:
			return 0;
		case ZenoColumnType.PREDISTILL:
			return 1;
		case ZenoColumnType.OUTPUT:
			return 2;
		case ZenoColumnType.METADATA:
			return 3;
		case ZenoColumnType.ITEM:
			return 4;
		case ZenoColumnType.LABEL:
			return 4;
		case ZenoColumnType.EMBEDDING:
			return 4;
	}
}

export function columnSort(col1: ZenoColumn, col2: ZenoColumn) {
	if (columnTypeOrder(col1.columnType) > columnTypeOrder(col2.columnType)) {
		return 1;
	} else if (columnTypeOrder(col1.columnType) < columnTypeOrder(col2.columnType)) {
		return -1;
	}

	if (col1.name < col2.name) {
		return -1;
	} else if (col1.name > col2.name) {
		return 1;
	} else {
		return 0;
	}
}

/** Calculate the metric range for coloring histograms */
export function getMetricRange(res: (number | null)[][]): [number, number] {
	const range: [number, number] = [Infinity, -Infinity];
	let allNull = true;
	res.forEach((arr) =>
		arr.forEach((n) => {
			if (n !== null) {
				allNull = false;
				range[0] = Math.min(range[0], n);
				range[1] = Math.max(range[1], n);
			}
		})
	);
	if (allNull) {
		return [Infinity, -Infinity];
	}
	return range;
}

// update model dependent slices in compare tab
export function updateModelDependentSlices(name: string, mod: string, slis: Slice[]) {
	slis.forEach((sli) => {
		const preds = sli.filterPredicates.predicates;
		if (doesModelDependOnPredicates(preds)) {
			const slices = [...get(slicesForComparison)];
			const index = slices.findIndex((current) => current.id === sli.id);
			if (index !== -1) {
				slicesForComparison.set([
					...slices.slice(0, index),
					<Slice>{
						id: sli.id,
						sliceName: sli.sliceName + ' (' + name + ')',
						folderId: sli.folderId,
						filterPredicates: setModelForFilterPredicateGroup(sli.filterPredicates, mod)
					},
					...slices.slice(index + 1)
				]);
			}
		}
	});
}

export function getEndpoint() {
	if (env.PUBLIC_BACKEND_ENDPOINT === 'http://127.0.0.1:8000') return '/localzeno';
	return env.PUBLIC_BACKEND_ENDPOINT;
}

export function getOperation(representation: string) {
	switch (representation) {
		case '==':
			return Operation.EQUAL;
		case '!=':
			return Operation.DIFFERENT;
		case '>':
			return Operation.GT;
		case '<':
			return Operation.LT;
		case '>=':
			return Operation.GTE;
		case '<=':
			return Operation.LTE;
		case 'LIKE':
			return Operation.LIKE;
		default:
			return Operation.EQUAL;
	}
}

export const inverseOperationMap = {
	[Operation.EQUAL]: '==',
	[Operation.DIFFERENT]: '!=',
	[Operation.GT]: '>',
	[Operation.LT]: '<',
	[Operation.GTE]: '>=',
	[Operation.LTE]: '<=',
	[Operation.LIKE]: 'LIKE'
};
