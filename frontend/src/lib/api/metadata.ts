/**
 * API functions for calculating metadata histograms.
 * We separate them into getting buckets, counts, and metrics so we
 * can run then asynchronously and provide interactive updates while waiting
 * for more expensive computations like calculating metrics.
 */
import { metricRange, requestingHistogramCounts } from '$lib/stores';
import { getMetricRange } from '$lib/util/util';
import {
	CancelablePromise,
	ZenoService,
	type FilterPredicateGroup,
	type HistogramBucket,
	type Metric,
	type ZenoColumn
} from '$lib/zenoapi';
import { get } from 'svelte/store';

/**
 * Fetch metadata columns buckets for histograms.
 *
 * @param completeColumns All complete columns.
 * @param model Current model.
 *
 * @returns Histogram buckets for each column.
 */
export async function getHistograms(
	project_uuid: string | undefined,
	completeColumns: ZenoColumn[],
	model: string | undefined
): Promise<Map<string, HistogramBucket[]>> {
	if (!project_uuid) {
		return new Map();
	}
	const requestedHistograms = completeColumns.filter((c) => c.model === null || c.model === model);

	requestingHistogramCounts.set(true);
	const res = await ZenoService.getHistogramBuckets(project_uuid, requestedHistograms);
	requestingHistogramCounts.set(false);

	return new Map<string, HistogramBucket[]>(requestedHistograms.map((col, i) => [col.id, res[i]]));
}

// Since a user might change the selection before we get counts,
// make this fetch request cancellable.
let histogramRequest: CancelablePromise<Array<Array<HistogramBucket>>>;
/**
 * Fetch histogram counts for the buckets of metadata columns.
 *
 * @param histograms Histogram buckets for each column.
 * @param filterPredicates Filter predicates to filter DataFrame by.
 * @returns Histogram counts for each column.
 */
export async function calculateHistograms(
	project_uuid: string | undefined,
	columns: ZenoColumn[],
	histograms: Map<string, HistogramBucket[]>,
	filterPredicates?: FilterPredicateGroup,
	dataIds?: string[],
	model?: string | null,
	metric?: Metric | null
): Promise<Map<string, HistogramBucket[]>> {
	if (!project_uuid) {
		return new Map();
	}
	const columnRequests = [...histograms.entries()].map(([k, v]) => ({
		column: columns.find((col) => col.id === k) ?? columns[0],
		buckets: v
	}));
	if (histogramRequest) {
		histogramRequest.cancel();
	}
	try {
		requestingHistogramCounts.set(true);
		histogramRequest = ZenoService.calculateHistograms(project_uuid, {
			columnRequests,
			filterPredicates,
			model,
			metric,
			dataIds
		});
		const out = await histogramRequest;
		requestingHistogramCounts.set(false);

		if (get(metricRange)[0] === Infinity) {
			metricRange.set(getMetricRange(out));
		}

		[...histograms.keys()].forEach((k, i) => {
			const hist = histograms.get(k);
			if (hist) {
				histograms.set(
					k,
					hist.map((h, j) => {
						if (filterPredicates === undefined) {
							h.size = out[i][j].size;
						}
						h.metric = out[i][j].metric;
						h.filteredSize = out[i][j].size;
						return h;
					})
				);
			}
		});
		return histograms;
	} catch (e) {
		return histograms;
	}
}
