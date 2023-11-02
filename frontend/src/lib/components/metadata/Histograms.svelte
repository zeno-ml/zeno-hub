<script lang="ts">
	import { page } from '$app/stores';
	import MetadataCell from '$lib/components/metadata/cells/MetadataCell.svelte';
	import {
		columns,
		metric,
		metricRange,
		model,
		project,
		requestingHistogramCounts,
		selectionPredicates,
		tagIds
	} from '$lib/stores';
	import { getMetricRange } from '$lib/util/util';
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
		const secureTagIds = $tagIds === undefined ? [] : $tagIds;
		const dataIds = [...new Set(secureTagIds)];
		zenoClient
			.calculateHistograms($project.uuid, {
				columns: requestColumns,
				filterPredicates: s.selectionPredicates,
				model: s.model,
				metric: s.metric,
				dataIds
			})
			.then((out) => {
				requestingHistogramCounts.set(false);

				if ($metricRange[0] === Infinity) {
					metricRange.set(getMetricRange(out));
				}
				if (metadataHistograms.size == 0) {
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
	});
</script>

{#if !$page.url.href.includes('compare')}
	{#each $columns.filter((c) => (c.model === undefined || c.model === null || c.model === $model) && histogramColumnsBaseFilter(c)) as col (col.id)}
		{@const hist = metadataHistograms.get(col.id)}
		{#if hist}
			<MetadataCell {col} histogram={hist} />
		{/if}
	{/each}
{/if}
