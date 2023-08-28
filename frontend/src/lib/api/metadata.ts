/**
 * API functions for calculating metadata histograms.
 * We separate them into getting buckets, counts, and metrics so we
 * can run then asynchronously and provide interactive updates while waiting
 * for more expensive computations like calculating metrics.
 */
import { columns, metricRange, project, requestingHistogramCounts } from '$lib/stores';
import { getMetricRange } from '$lib/util/util';
import {
	CancelablePromise,
	ZenoColumnType,
	ZenoService,
	type FilterPredicateGroup,
	type ZenoColumn
} from '$lib/zenoapi';
import { get } from 'svelte/store';

export interface HistogramEntry {
	bucket: number | string | boolean;
	bucketEnd?: number | string | boolean | null;
	count?: number;
	filteredCount?: number;
	metric?: number;
}

/**
 * Fetch metadata columns buckets for histograms.
 *
 * @param completeColumns All complete columns.
 * @param model Current model.
 *
 * @returns Histogram buckets for each column.
 */
export async function getHistograms(
	completeColumns: ZenoColumn[],
	model: string | undefined
): Promise<Map<string, HistogramEntry[]>> {
	const requestedHistograms = completeColumns.filter(
		(c) => (c.model === null || c.model === model) && c.columnType !== ZenoColumnType.DATA
	);
	requestingHistogramCounts.set(true);
	const config = get(project);
	if (!config) {
		return Promise.reject('No project selected.');
	}
	const res = await ZenoService.getHistogramBuckets(config.uuid, requestedHistograms);
	requestingHistogramCounts.set(false);
	const histograms = new Map<string, HistogramEntry[]>(
		[
			...new Map<string, HistogramEntry[]>(requestedHistograms.map((col, i) => [col.id, res[i]]))
		].filter((el) => el[1].length < 30)
	);
	return histograms;
}

// Since a user might change the selection before we get counts,
// make this fetch request cancellable.
let histogramCountRequest: CancelablePromise<Array<Array<number>>>;
/**
 * Fetch histogram counts for the buckets of metadata columns.
 *
 * @param histograms Histogram buckets for each column.
 * @param filterPredicates Filter predicates to filter DataFrame by.
 * @returns Histogram counts for each column.
 */
export async function getHistogramCounts(
	histograms: Map<string, HistogramEntry[]>,
	filterPredicates?: FilterPredicateGroup,
	dataIds?: string[]
): Promise<Map<string, HistogramEntry[]> | undefined> {
	const columnRequests = [...histograms.entries()].map(([k, v]) => ({
		column: get(columns).find((col) => col.id === k) ?? get(columns)[0],
		buckets: v
	}));
	if (histogramCountRequest) {
		histogramCountRequest.cancel();
	}
	try {
		const config = get(project);
		if (!config) {
			return Promise.reject('No project selected.');
		}
		requestingHistogramCounts.set(true);
		histogramCountRequest = ZenoService.calculateHistogramCounts(config.uuid, {
			columnRequests,
			filterPredicates,
			dataIds
		});
		const out = await histogramCountRequest;
		requestingHistogramCounts.set(false);

		[...histograms.keys()].forEach((k, i) => {
			const hist = histograms.get(k);
			if (hist) {
				histograms.set(
					k,
					hist.map((h, j) => {
						if (filterPredicates === undefined) {
							h.count = out[i][j];
						}
						h.filteredCount = out[i][j];
						return h;
					})
				);
			}
		});
		return histograms;
	} catch (e) {
		return undefined;
	}
}

// Since a user might change the selection before we get metrics,
// make this fetch request cancellable.
let histogramMetricRequest: CancelablePromise<Array<Array<number | null>>>;
/**
 * Fetch histogram metrics for the buckets of metadata columns.
 *
 * @param histograms Histogram buckets for each column.
 * @param filterPredicates Filter predicates to filter DataFrame by.
 * @param model Model to fetch metrics for.
 * @param metric Metric to calculate per bucket.
 * @returns Histogram metrics for each column.
 */
export async function getHistogramMetrics(
	histograms: Map<string, HistogramEntry[]>,
	model: string | undefined,
	metric: string,
	dataIds: string[] | undefined,
	filterPredicates?: FilterPredicateGroup
): Promise<Map<string, HistogramEntry[]> | undefined> {
	const config = get(project);
	if (metric === '' || !config || !config.calculateHistogramMetrics) {
		return undefined;
	}
	const columnRequests = [...histograms.entries()].map(([k, v]) => ({
		column: get(columns).find((col) => col.id === k) ?? get(columns)[0],
		buckets: v
	}));
	if (histogramMetricRequest) {
		histogramMetricRequest.cancel();
	}
	try {
		const config = get(project);
		if (!config) {
			return Promise.reject('No project selected.');
		}
		histogramMetricRequest = ZenoService.calculateHistogramMetrics(config.uuid, {
			columnRequests,
			filterPredicates,
			model: model ?? null,
			metric,
			dataIds
		});

		requestingHistogramCounts.set(true);
		const res = await histogramMetricRequest;
		requestingHistogramCounts.set(false);

		if (res === undefined) {
			return undefined;
		}

		if (get(metricRange)[0] === Infinity) {
			metricRange.set(getMetricRange(res));
		}

		[...histograms.keys()].forEach((k, i) => {
			const hist = histograms.get(k);
			if (hist !== undefined) {
				histograms.set(
					k,
					hist.map((h, j) => {
						h.metric = res[i][j] || 0;
						return h;
					})
				);
			}
		});
		return histograms;
	} catch (e) {
		return undefined;
	}
}
