<script lang="ts">
	import { page } from '$app/stores';
	import { calculateHistograms, getHistograms } from '$lib/api/metadata';
	import MetadataCell from '$lib/components/metadata/cells/MetadataCell.svelte';
	import { columns, metric, model, project, selectionIds, selectionPredicates } from '$lib/stores';
	import { ZenoColumnType, type HistogramBucket } from '$lib/zenoapi';

	let metadataHistograms: Map<string, HistogramBucket[]> = new Map();

	getHistograms($project?.uuid, $columns, $model).then((res) => {
		calculateHistograms(
			$project?.uuid,
			$columns,
			res,
			undefined,
			$selectionIds,
			$model,
			$metric
		).then((res) => {
			metadataHistograms = res;
		});
	});

	metric.subscribe((m) => {
		calculateHistograms(
			$project?.uuid,
			$columns,
			metadataHistograms,
			$selectionPredicates,
			$selectionIds,
			$model,
			m
		).then((r) => (metadataHistograms = r));
	});

	model.subscribe((m) => {
		getHistograms($project?.uuid, $columns, $model).then((res) => {
			calculateHistograms(
				$project?.uuid,
				$columns,
				res,
				$selectionPredicates,
				$selectionIds,
				m,
				$metric
			).then((r) => (metadataHistograms = r));
		});
	});

	// when the selection Ids change, update the histograms
	selectionIds.subscribe((selectionIds) =>
		calculateHistograms(
			$project?.uuid,
			$columns,
			metadataHistograms,
			$selectionPredicates,
			selectionIds,
			$model,
			$metric
		).then((r) => (metadataHistograms = r))
	);

	// Update counts and metrics when selection changes.
	selectionPredicates.subscribe((sels) => {
		if (metadataHistograms.size === 0) {
			return;
		}
		calculateHistograms(
			$project?.uuid,
			$columns,
			metadataHistograms,
			sels,
			$selectionIds,
			$model,
			$metric
		).then((r) => (metadataHistograms = r));
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
