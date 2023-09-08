import { browser } from '$app/environment';
import { env } from '$env/dynamic/public';
import {
	Operation,
	ZenoColumnType,
	type FilterPredicateGroup,
	type Metric,
	type ZenoColumn
} from '$lib/zenoapi';
import { get } from 'svelte/store';
import {
	authToken,
	compareSort,
	comparisonColumn,
	comparisonModel,
	metric,
	metricRange,
	model,
	project,
	selections
} from '../stores';

export type URLParams = {
	model: string | undefined;
	metric: Metric | undefined;
	comparisonModel: string | undefined;
	comparisonColumn: ZenoColumn | undefined;
	compareSort: [ZenoColumn | undefined, boolean] | undefined;
	metricRange: [number, number] | undefined;
	selections:
		| { metadata: Record<string, FilterPredicateGroup>; slices: number[]; tags: number[] }
		| undefined;
};

export function getProjectRouteFromURL(url: URL) {
	let projectURL = url.origin;
	const pathParts = url.pathname.split('/');
	const projectIndex = pathParts.indexOf('project');
	for (let i = 1; i < projectIndex + 3; i++) {
		projectURL = projectURL + '/' + pathParts[i];
	}
	return projectURL;
}

function columnTypeOrder(colType: ZenoColumnType) {
	switch (colType) {
		case ZenoColumnType.FEATURE:
			return 0;
		case ZenoColumnType.OUTPUT:
			return 1;
		case ZenoColumnType.DATA:
			return 2;
		case ZenoColumnType.LABEL:
			return 2;
		case ZenoColumnType.EMBEDDING:
			return 2;
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

export function getEndpoint() {
	if (env.PUBLIC_BACKEND_ENDPOINT == 'http://zeno-backend:8000') {
		if (browser) {
			return '/dockerzeno';
		}
		return 'http://zeno-backend:8000';
	}
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

export function shortenNumber(num: number, digits: number) {
	const lookup = [
		{ value: 1, symbol: '' },
		{ value: 1e3, symbol: 'k' },
		{ value: 1e6, symbol: 'M' },
		{ value: 1e9, symbol: 'G' },
		{ value: 1e12, symbol: 'T' },
		{ value: 1e15, symbol: 'P' },
		{ value: 1e18, symbol: 'E' }
	];
	const rx = /\.0+$|(\.[0-9]*[1-9])0+$/;
	const item = lookup
		.slice()
		.reverse()
		.find(function (item) {
			return num >= item.value;
		});
	return item ? (num / item.value).toFixed(digits).replace(rx, '$1') + item.symbol : '0';
}

export async function resolveDataPoint(entry: Record<string, unknown>): Promise<Response | string> {
	if (entry['data'] !== null && entry['data'] !== undefined) {
		return entry['data'] as string;
	}
	if (isValidHttpUrl(get(project)?.dataUrl ?? '' + entry['data_id'])) {
		return await fetch(get(project)?.dataUrl ?? '' + entry['data_id']);
	}
	return await fetch(
		`${getEndpoint()}/api/data/${get(project)?.uuid}?data_id=${encodeURIComponent(
			entry['data_id'] as string
		)}`,
		{
			headers: {
				Authorization: 'Bearer ' + get(authToken)
			}
		}
	);
}

function isValidHttpUrl(string: string) {
	let url;
	try {
		url = new URL(string);
	} catch (_) {
		return false;
	}
	return url.protocol === 'http:' || url.protocol === 'https:';
}

export function setURLParameters() {
	if (!browser) return;
	const params = {
		model: get(model),
		metric: get(metric),
		comparisonModel: get(comparisonModel),
		comparisonColumn: get(comparisonColumn),
		compareSort: get(compareSort),
		metricRange: get(metricRange),
		selections: get(selections)
	} as URLParams;
	window.history.replaceState(history.state, '', `?params=${btoa(JSON.stringify(params))}`);
}
