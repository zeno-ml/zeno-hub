<script lang="ts">
	import { page } from '$app/stores';
	import MetadataCell from '$lib/components/metadata/cells/MetadataCell.svelte';
	import {
		columns,
		filterSelection,
		metric,
		metricRange,
		model,
		project,
		requestingHistogramCounts,
		selectionIds,
		selectionPredicates,
		tagIds
	} from '$lib/stores';
	import { getMetricRange, reverseColumnSort } from '$lib/util/util';
	import {
		MetadataType,
		ZenoColumnType,
		ZenoService,
		type FilterPredicateGroup,
		type HistogramBucket,
		type Metric,
		type ZenoColumn
	} from '$lib/zenoapi';
	import { getContext } from 'svelte';
	import { derived, type Readable } from 'svelte/store';

	type HistogramState = {
		model: string | undefined;
		metric: Metric | undefined;
		selectionPredicates: FilterPredicateGroup | undefined;
	};

	const zenoClient = getContext('zenoClient') as ZenoService;
	const histogramColumnsBaseFilter = (c: ZenoColumn) =>
		(c.columnType === ZenoColumnType.ID ||
			c.columnType === ZenoColumnType.DATA ||
			c.columnType === ZenoColumnType.FEATURE ||
			c.columnType === ZenoColumnType.LABEL ||
			c.columnType === ZenoColumnType.OUTPUT) &&
		c.dataType !== MetadataType.EMBEDDING;
	let metadataHistograms: Map<string, HistogramBucket[]> = new Map();

	// Derived store to only update histograms once at startup.
	const histogramState: Readable<HistogramState> = derived(
		[model, metric, selectionPredicates],
		([$model, $metric, $selectionPredicates]) => {
			return {
				model: $model,
				metric: $metric,
				selectionPredicates: $selectionPredicates
			};
		}
	);

	model.subscribe(() => {
		metadataHistograms = new Map();
	});

	histogramState.subscribe((s) => {
		const requestColumns = $columns.filter(
			(c) => (c.model === null || c.model === s.model) && histogramColumnsBaseFilter(c)
		);

		requestingHistogramCounts.set(true);
		const secureIds = [
			...($tagIds === undefined ? [] : $tagIds),
			...($filterSelection ? $selectionIds : [])
		];
		const dataIds = [...new Set(secureIds)];
		if (metadataHistograms.size === 0) {
			// If histograms have not been loaded fully, load them, then load them filtered.
			requestHistograms(requestColumns, s.model, s.metric, undefined, []).then(() => {
				if (s.selectionPredicates || dataIds) {
					requestHistograms(requestColumns, s.model, s.metric, s.selectionPredicates, dataIds);
				}
			});
		} else {
			// Update filtered size if histograms have been loaded already
			requestHistograms(requestColumns, s.model, s.metric, s.selectionPredicates, dataIds);
		}
	});

	async function requestHistograms(
		requestColumns: ZenoColumn[],
		model?: string,
		metric?: Metric,
		selectionPredicates?: FilterPredicateGroup,
		dataIds?: string[]
	) {
		await zenoClient
			.calculateHistograms($project.uuid, {
				columns: requestColumns,
				filterPredicates: selectionPredicates,
				model: model,
				metric: metric,
				dataIds
			})
			.then((out) => {
				requestingHistogramCounts.set(false);

				if ($metricRange[0] === Infinity) {
					metricRange.set(getMetricRange(out));
				}
				if (metadataHistograms.size === 0) {
					requestColumns.forEach((c, i) => {
						metadataHistograms.set(
							c.id,
							out[i].map((h) => ({
								...h,
								filteredSize: h.size
							}))
						);
					});
				} else {
					[...metadataHistograms.keys()].forEach((k, i) => {
						const hist = metadataHistograms.get(k);
						if (hist) {
							metadataHistograms.set(
								k,
								hist.map((h, j) => {
									h.metric = out[i][j].metric;
									h.filteredSize = out[i][j].size;
									return h;
								})
							);
						}
					});
				}
				metadataHistograms = new Map(metadataHistograms);
			});
	}
</script>

{#if !$page.url.href.includes('compare')}
	{#each $columns
		.filter((c) => (c.model === undefined || c.model === null || c.model === $model) && histogramColumnsBaseFilter(c))
		.sort(reverseColumnSort) as col (col.id)}
		<MetadataCell {col} histogram={metadataHistograms.get(col.id)} />
	{/each}
{/if}
