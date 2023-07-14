/**
 * API functions for calculating metadata histograms.
 * We separate them into getting buckets, counts, and metrics so we
 * can run then asynchronously and provide interactive updates while waiting
 * for more expensive computations like calculating metrics.
 */
import { currentProject, metricRange, projectConfig, requestingHistogramCounts } from '$lib/stores';
import { columnHash, getMetricRange } from '$lib/util/util';
import {
	CancelablePromise,
	ZenoService,
	type FilterPredicateGroup,
	type ZenoColumn,
	type Metric,
	ZenoColumnType
} from '$lib/zenoapi';
import { InternMap } from 'internmap';
import { get } from 'svelte/store';

export interface HistogramEntry {
	bucket: number | string | boolean;
	bucketEnd?: number | string | boolean;
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
	model: string
): Promise<InternMap<ZenoColumn, HistogramEntry[]>> {
	const requestedHistograms = completeColumns.filter(
		(c) => (c.model === null || c.model === model) && c.columnType !== ZenoColumnType.ITEM
	);
	requestingHistogramCounts.set(true);
	const project = get(currentProject);
	if (!project) {
		return Promise.reject('No project selected.');
	}
	const res = await ZenoService.getHistogramBuckets(project.uuid, requestedHistograms);
	requestingHistogramCounts.set(false);
	const histograms = new InternMap<string, HistogramEntry[]>(
		requestedHistograms.map((col, i) => [col, res[i]]),
		columnHash
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
	histograms: InternMap<ZenoColumn, HistogramEntry[]>,
	filterPredicates?: FilterPredicateGroup,
	items?: string[]
): Promise<number[][] | undefined> {
	const columnRequests = [...histograms.entries()].map(([k, v]) => ({
		column: k,
		buckets: v
	}));
	if (histogramCountRequest) {
		histogramCountRequest.cancel();
	}
	try {
		const project = get(currentProject);
		if (!project) {
			return Promise.reject('No project selected.');
		}
		requestingHistogramCounts.set(true);
		histogramCountRequest = ZenoService.calculateHistogramCounts(project.uuid, {
			columnRequests,
			filterPredicates,
			items
		});
		const out = await histogramCountRequest;
		requestingHistogramCounts.set(false);

		[...histograms.keys()].forEach((k, i) => {
			histograms.set(
				k,
				histograms.get(k).map((h, j) => {
					if (filterPredicates === undefined) {
						h.count = out[i][j];
					}
					h.filteredCount = out[i][j];
					return h;
				})
			);
		});
		return histograms;
	} catch (e) {
		return undefined;
	}
}

// Since a user might change the selection before we get metrics,
// make this fetch request cancellable.
let histogramMetricRequest: CancelablePromise<Array<Array<number>>>;
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
	histograms: InternMap<ZenoColumn, HistogramEntry[]>,
	model: string,
	metric: Metric,
	items: string[] | undefined,
	filterPredicates?: FilterPredicateGroup
): Promise<InternMap<ZenoColumn, HistogramEntry[]> | undefined> {
	const config = get(projectConfig);
	if (metric.name === '' || !config || !config.calculateHistogramMetrics) {
		return undefined;
	}
	const columnRequests = [...histograms.entries()].map(([k, v]) => ({
		column: k,
		buckets: v
	}));
	if (histogramMetricRequest) {
		histogramMetricRequest.cancel();
	}
	try {
		const project = get(currentProject);
		if (!project) {
			return Promise.reject('No project selected.');
		}
		histogramMetricRequest = ZenoService.calculateHistogramMetrics(project.uuid, {
			columnRequests,
			filterPredicates,
			model,
			metric,
			items
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
			histograms.set(
				k,
				histograms.get(k).map((h, j) => {
					h.metric = res[i][j];
					return h;
				})
			);
		});
		return histograms;
	} catch (e) {
		return undefined;
	}
}
