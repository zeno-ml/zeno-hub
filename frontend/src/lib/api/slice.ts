import { project } from '$lib/stores';
import { ZenoService, type FilterPredicate, type GroupMetric, type MetricKey } from '$lib/zenoapi';
import { get } from 'svelte/store';

export function instanceOfFilterPredicate(object: object): object is FilterPredicate {
	return 'column' in object;
}

const metricKeyCache = new Map();
export async function getMetricsForSlices(metricKeys: MetricKey[]): Promise<GroupMetric[] | null> {
	if (metricKeys.length === 0) {
		return null;
	}

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
		const config = get(project);
		if (!config) {
			return Promise.reject('No project selected.');
		}
		const res = await ZenoService.getMetricsForSlices(config.uuid, {
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
	dataIds?: string[]
): Promise<GroupMetric[] | undefined> {
	if (metricKeys.length === 0) {
		return undefined;
	}
	if (metricKeys.length > 0) {
		const config = get(project);
		if (!config) {
			return Promise.reject('No project selected.');
		}
		return await ZenoService.getMetricsForSlices(config.uuid, {
			metricKeys,
			dataIds
		});
	}
}
