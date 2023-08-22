<script lang="ts">
	import { page } from '$app/stores';
	import {
		getHistogramCounts,
		getHistogramMetrics,
		getHistograms,
		type HistogramEntry
	} from '$lib/api/metadata';
	import {
		columns,
		comparisonModel,
		metric,
		metricRange,
		model,
		requestingHistogramCounts,
		selectionIds,
		selectionPredicates,
		selections,
		slices,
		tagIds
	} from '$lib/stores';
	import { updateModelDependentSlices } from '$lib/util/util';
	import { Join, ZenoColumnType, type FilterPredicateGroup, type Metric } from '$lib/zenoapi';
	import { mdiInformationOutline } from '@mdi/js';
	import CircularProgress from '@smui/circular-progress';
	import { Icon } from '@smui/icon-button';
	import { tooltip } from '@svelte-plugins/tooltips';
	import { onMount } from 'svelte';
	import MetadataCell from './cells/MetadataCell.svelte';
	import MetricRange from './MetricRange.svelte';

	let metadataHistograms: Map<string, HistogramEntry[]> = new Map();

	// Get histogram buckets, counts, and metrics when columns update.
	onMount(() => {
		loadHistogramData($tagIds, $selectionIds, $model, $metric);
		$model !== undefined && updateModelDependentSlices('model A', $model, $slices);
	});

	function loadHistogramData(
		tagIds: string[] | undefined,
		selectionIds: string[] | undefined,
		model: string | undefined,
		metric: Metric | undefined
	) {
		const dataIds =
			tagIds !== undefined && selectionIds !== undefined
				? [...new Set([...tagIds, ...selectionIds])]
				: tagIds !== undefined
				? tagIds
				: selectionIds;
		getHistograms($columns, model).then((res) => {
			getHistogramCounts(res, undefined, dataIds).then((res) => {
				if (res === undefined) {
					return;
				}
				metadataHistograms = res;
				metric !== undefined &&
					getHistogramMetrics(res, model, metric, dataIds, undefined).then((res) => {
						if (res !== undefined) {
							metadataHistograms = res;
						}
					});
			});
		});
	}

	function loadCountsAndMetrics(
		tagIds: string[] | undefined,
		selectionIds: string[] | undefined,
		model: string | undefined,
		metric: Metric | undefined,
		selectionPredicates: FilterPredicateGroup | undefined
	) {
		const dataIds =
			tagIds !== undefined && selectionIds !== undefined
				? [...new Set([...tagIds, ...selectionIds])]
				: tagIds !== undefined
				? tagIds
				: selectionIds;
		getHistogramCounts(
			metadataHistograms,
			selectionPredicates === undefined
				? undefined
				: {
						predicates: [selectionPredicates],
						join: Join.AND
				  },
			dataIds
		).then((res) => {
			if (res === undefined) {
				return;
			}

			metadataHistograms = res;
			model !== undefined &&
				metric !== undefined &&
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

	comparisonModel.subscribe((mod) => {
		mod && updateModelDependentSlices('model B', mod, $slices);
	});

	// Calculate histogram metrics when metric changes
	metric.subscribe((metric) => {
		if (metadataHistograms.size === 0) {
			return;
		}
		metricRange.set([Infinity, -Infinity]);
		const dataIds =
			$tagIds !== undefined && $selectionIds !== undefined
				? [...new Set([...$tagIds, ...$selectionIds])]
				: $tagIds !== undefined
				? $tagIds
				: $selectionIds;
		$model !== undefined &&
			metric !== undefined &&
			getHistogramMetrics(metadataHistograms, $model, metric, dataIds, undefined).then((res) => {
				if (res === undefined) {
					return;
				}
				metadataHistograms = res;
			});
	});

	// Calculate histogram counts when model changes for feature columns
	model.subscribe((model) => {
		if (metadataHistograms.size === 0) {
			return;
		}
		selections.set({ metadata: {}, slices: [], tags: [] });
		loadHistogramData(undefined, undefined, model, $metric);
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
	<div
		class="flex items-center justify-between pt-2.5 sticky top-24 border-b border-grey-lighter bg-yellowish-light z-10"
	>
		<div class="flex items-center justify-between">
			<h4>Metadata</h4>
			<div
				class="w-6 h-6 cursor-help fill-grey-dark"
				use:tooltip={{
					content:
						'Interactive distributions for metadata columns. Click or drag on the histograms to filter the data.',
					position: 'right',
					theme: 'zeno-tooltip'
				}}
			>
				<Icon style="outline:none" tag="svg" viewBox="-6 -6 36 36">
					<path d={mdiInformationOutline} />
				</Icon>
			</div>
			{#if $requestingHistogramCounts}
				<CircularProgress style="height: 15px; width: 15px; margin-left: 10px;" indeterminate />
			{/if}
		</div>
		<MetricRange />
	</div>
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
