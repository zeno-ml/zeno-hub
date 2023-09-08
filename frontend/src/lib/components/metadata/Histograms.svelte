<script lang="ts">
	import { page } from '$app/stores';
	import {
		getHistogramCounts,
		getHistogramMetrics,
		loadHistogramData,
		type HistogramEntry
	} from '$lib/api/metadata';
	import MetadataCell from '$lib/components/metadata/cells/MetadataCell.svelte';
	import {
		columns,
		metric,
		model,
		project,
		selectionIds,
		selectionPredicates,
		tagIds
	} from '$lib/stores';
	import { Join, ZenoColumnType, type FilterPredicateGroup, type Metric } from '$lib/zenoapi';

	let metadataHistograms: Map<string, HistogramEntry[]> = new Map();

	if ($project) {
		loadHistogramData($project?.uuid, undefined, undefined, $model, $columns).then((res) => {
			if (res !== undefined) {
				metadataHistograms = res;
			}
		});
	}

	function loadCountsAndMetrics(
		tagIds: string[] | undefined,
		selectionIds: string[] | undefined,
		model: string | undefined,
		metric: Metric | undefined,
		selectionPredicates: FilterPredicateGroup | undefined
	) {
		if ($project === undefined) return;
		const dataIds =
			tagIds !== undefined && selectionIds !== undefined
				? [...new Set([...tagIds, ...selectionIds])]
				: tagIds !== undefined
				? tagIds
				: selectionIds;
		getHistogramCounts(
			$project.uuid,
			$columns,
			metadataHistograms,
			selectionPredicates === undefined
				? undefined
				: {
						predicates: [selectionPredicates],
						join: Join.AND
				  },
			dataIds
		).then((res) => {
			if (res === undefined || model === undefined || metric === undefined) {
				return;
			}
			metadataHistograms = res;
			getHistogramMetrics(
				res,
				model,
				metric,
				dataIds,
				selectionPredicates === undefined
					? undefined
					: {
							predicates: [selectionPredicates],
							join: Join._
					  }
			).then((res) => {
				if (res === undefined) {
					return;
				}
				metadataHistograms = res;
			});
		});
	}

	// Calculate histogram metrics when metric changes
	metric.subscribe((metric) => {
		if (metadataHistograms.size === 0 || $model === undefined || metric === undefined) {
			return;
		}

		const dataIds =
			$tagIds !== undefined && $selectionIds !== undefined
				? [...new Set([...$tagIds, ...$selectionIds])]
				: $tagIds !== undefined
				? $tagIds
				: $selectionIds;

		getHistogramMetrics(metadataHistograms, $model, metric, dataIds, undefined).then((res) => {
			if (res === undefined) {
				return;
			}
			metadataHistograms = res;
		});
	});

	// Calculate histogram counts when model changes for feature columns
	model.subscribe((model) => {
		if ($project) {
			loadHistogramData($project.uuid, undefined, undefined, model, $columns).then((res) => {
				if (res !== undefined) {
					metadataHistograms = res;
				}
			});
		}
	});

	// when the selection Ids change, update the histograms
	selectionIds.subscribe((selectionIds) => {
		if (metadataHistograms.size === 0) {
			return;
		}
		loadCountsAndMetrics($tagIds, selectionIds, $model, $metric, $selectionPredicates);
	});

	// when the tag Ids change, update the histograms
	tagIds.subscribe((tIds) => {
		if (metadataHistograms.size === 0) {
			return;
		}
		loadCountsAndMetrics(tIds, $selectionIds, $model, $metric, $selectionPredicates);
	});

	// Update counts and metrics when selection changes.
	selectionPredicates.subscribe((sels) => {
		if (metadataHistograms.size === 0) {
			return;
		}
		loadCountsAndMetrics($tagIds, $selectionIds, $model, $metric, sels);
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
