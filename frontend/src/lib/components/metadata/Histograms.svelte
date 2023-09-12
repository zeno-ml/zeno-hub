<script lang="ts">
	import { page } from '$app/stores';
	import { calculateHistograms, getHistograms } from '$lib/api/metadata';
	import MetadataCell from '$lib/components/metadata/cells/MetadataCell.svelte';
	import { columns, metric, model, project, selectionIds, selectionPredicates } from '$lib/stores';
	import {
		ZenoColumnType,
		type FilterPredicateGroup,
		type HistogramBucket,
		type Metric
	} from '$lib/zenoapi';
	import { derived, type Readable } from 'svelte/store';

	let metadataHistograms: Map<string, HistogramBucket[]> = new Map();

	type HistogramState = {
		model: string | undefined;
		metric: Metric | undefined;
		selectionPredicates: FilterPredicateGroup | undefined;
	};

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
		if (metadataHistograms.size === 0) {
			getHistograms($project?.uuid, $columns, $model).then((res) => {
				calculateHistograms(
					$project?.uuid,
					$columns,
					res,
					s.selectionPredicates,
					$selectionIds,
					s.model,
					s.metric
				).then((res) => {
					metadataHistograms = res;
				});
			});
		} else {
			calculateHistograms(
				$project?.uuid,
				$columns,
				metadataHistograms,
				s.selectionPredicates,
				$selectionIds,
				s.model,
				s.metric
			).then((res) => {
				metadataHistograms = res;
			});
		}
	});
</script>

{#if !$page.url.href.includes('compare')}
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
