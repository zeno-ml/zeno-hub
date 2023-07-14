import { currentProject } from '$lib/stores';
import { isPredicateGroup } from '$lib/util/typeCheck';
import {
	ZenoColumnType,
	ZenoService,
	type FilterPredicate,
	type FilterPredicateGroup,
	type GroupMetric,
	type MetricKey
} from '$lib/zenoapi';
import { get } from 'svelte/store';

export function instanceOfFilterPredicate(object: object): object is FilterPredicate {
	return 'column' in object;
}

export function setModelForFilterPredicateGroup(
	pred: FilterPredicateGroup | FilterPredicate,
	model: string
): FilterPredicate | FilterPredicateGroup {
	if (instanceOfFilterPredicate(pred)) {
		if (
			pred.column.columnType === ZenoColumnType.POSTDISTILL ||
			pred.column.columnType === ZenoColumnType.OUTPUT
		) {
			pred = {
				...pred,
				column: {
					...pred.column,
					model: model
				}
			};
		}
	} else {
		return {
			...pred,
			predicates: pred.predicates.map((p) => setModelForFilterPredicateGroup(p, model))
		};
	}
	return pred;
}

function setModelForMetricKeys(metricKeys: MetricKey[]) {
	return metricKeys.map((key) => {
		if (key.slice.filterPredicates && key.slice.filterPredicates.predicates.length > 0) {
			return {
				...key,
				slice: {
					...key.slice,
					filterPredicates: {
						...key.slice.filterPredicates,
						predicates: key.slice.filterPredicates.predicates.map((pred) => {
							return {
								...pred,
								...setModelForFilterPredicateGroup(pred, key.model)
							};
						})
					}
				}
			};
		}
		return { ...key };
	});
}

const metricKeyCache = new Map();
export async function getMetricsForSlices(metricKeys: MetricKey[]): Promise<GroupMetric[] | null> {
	if (metricKeys.length === 0) {
		return null;
	}

	// Update model in predicates if slices are dependent on postdistill or output columns.
	metricKeys = <MetricKey[]>setModelForMetricKeys(metricKeys);
	// Check if we have already fetched this metric key
	const keysToRequest: MetricKey[] = [];
	const requestIndices: number[] = [];
	const results = [];
	for (let i = 0; i < metricKeys.length; i++) {
		const metricKeyHash = JSON.stringify(metricKeys[i]);
		if (metricKeyCache.has(metricKeyHash)) {
			results[i] = metricKeyCache.get(metricKeyHash);
		} else {
			keysToRequest.push(metricKeys[i]);
			requestIndices.push(i);
		}
	}
	if (keysToRequest.length > 0) {
		const project = get(currentProject);
		if (!project) {
			return Promise.reject('No project selected.');
		}
		const res = await ZenoService.getMetricsForSlices(project.uuid, {
			metricKeys: keysToRequest
		});
		keysToRequest.forEach((key, i) => {
			metricKeyCache.set(JSON.stringify(key), res[i]);
			results[requestIndices[i]] = res[i];
		});
	}

	return results;
}

export async function getMetricsForSlicesAndTags(
	metricKeys: MetricKey[],
	items?: string[],
	compare?: boolean
): Promise<GroupMetric[] | undefined> {
	if (metricKeys.length === 0) {
		return undefined;
	}
	// Update model in predicates if slices are dependent on postdistill columns.
	if (!compare) {
		metricKeys = <MetricKey[]>setModelForMetricKeys(metricKeys);
	}
	if (metricKeys.length > 0) {
		const project = get(currentProject);
		if (!project) {
			return Promise.reject('No project selected.');
		}
		return await ZenoService.getMetricsForSlices(project.uuid, {
			metricKeys,
			items
		});
	}
}

// check if predicates contain model dependent columns (postdistill or output)
export function doesModelDependOnPredicates(
	predicates: Array<FilterPredicateGroup | FilterPredicate>
) {
	const isModelDependent: boolean[] = [];
	predicates.forEach((p) => {
		isModelDependent.push(
			isPredicateGroup(p)
				? doesModelDependOnPredicates(p.predicates)
				: p.column.columnType === ZenoColumnType.POSTDISTILL ||
						p.column.columnType === ZenoColumnType.OUTPUT
		);
	});
	return isModelDependent.includes(true);
}
