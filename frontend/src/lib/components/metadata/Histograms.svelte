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
		selectionIds,
		selectionPredicates,
		tagIds
	} from '$lib/stores';
	import { getMetricRange } from '$lib/util/util';
	import {
		ZenoColumnType,
		ZenoService,
		type FilterPredicateGroup,
		type HistogramBucket,
		type Metric
	} from '$lib/zenoapi';
	import { derived, type Readable } from 'svelte/store';

	type HistogramState = {
		model: string | undefined;
		metric: Metric | undefined;
		selectionPredicates: FilterPredicateGroup | undefined;
	};

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
			(c) =>
				(c.model === null || c.model === s.model) &&
				(c.columnType === ZenoColumnType.DATA ||
					c.columnType === ZenoColumnType.FEATURE ||
					c.columnType === ZenoColumnType.LABEL ||
					c.columnType === ZenoColumnType.OUTPUT)
		);

		requestingHistogramCounts.set(true);
		const secureTagIds = $tagIds === undefined ? [] : $tagIds;
		const secureSelectionIds = $selectionIds === undefined ? [] : $selectionIds;
		const dataIds = [...new Set([...secureTagIds, ...secureSelectionIds])];
		ZenoService.calculateHistograms($project.uuid, {
			columns: requestColumns,
			filterPredicates: s.selectionPredicates,
			model: s.model,
			metric: s.metric,
			dataIds
		}).then((out) => {
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
	{#each $columns.filter((m) => m.columnType === ZenoColumnType.DATA) as col (col.id)}
		{@const hist = metadataHistograms.get(col.id)}
		{#if hist}
			<MetadataCell {col} histogram={hist} />
		{/if}
	{/each}
	{#each $columns.filter((m) => m.columnType === ZenoColumnType.LABEL) as col (col.id)}
		{@const hist = metadataHistograms.get(col.id)}
		{#if hist}
			<MetadataCell {col} histogram={hist} />
		{/if}
	{/each}
	{#each $columns.filter((m) => m.columnType === ZenoColumnType.FEATURE && (m.model === undefined || m.model === null || m.model === $model)) as col (col.id)}
		{@const hist = metadataHistograms.get(col.id)}
		{#if hist}
			<MetadataCell {col} histogram={hist} />
		{/if}
	{/each}
	{#if $model}
		{@const outputCol = $columns.filter(
			(m) => m.columnType === ZenoColumnType.OUTPUT && m.model === $model
		)}
		{#if outputCol.length > 0}
			{@const hist = metadataHistograms.get(outputCol[0].id)}
			{#if hist}
				<MetadataCell col={outputCol[0]} histogram={hist} />
			{/if}
		{/if}
	{/if}
{/if}
