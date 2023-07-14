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
	import { columnHash, updateModelDependentSlices } from '$lib/util/util';
	import {
		Join,
		ZenoColumnType,
		type FilterPredicateGroup,
		type Metric,
		type ZenoColumn
	} from '$lib/zenoapi';
	import { mdiInformationOutline } from '@mdi/js';
	import CircularProgress from '@smui/circular-progress';
	import { Svg } from '@smui/common';
	import { Icon } from '@smui/icon-button';
	import { tooltip } from '@svelte-plugins/tooltips';
	import { InternMap } from 'internmap';
	import { onMount } from 'svelte';
	import MetricRange from './MetricRange.svelte';
	import MetadataCell from './cells/MetadataCell.svelte';

	let metadataHistograms: InternMap<ZenoColumn, HistogramEntry[]> = new InternMap([], columnHash);

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
		const items =
			tagIds !== undefined && selectionIds !== undefined
				? [...new Set([...tagIds, ...selectionIds])]
				: tagIds !== undefined
				? tagIds
				: selectionIds;
		model !== undefined &&
			getHistograms($columns, model).then((res) => {
				getHistogramCounts(res, undefined, items).then((res) => {
					if (res === undefined) {
						return;
					}
					metadataHistograms = res;
					metric !== undefined &&
						getHistogramMetrics(res, model, metric, items, undefined).then((res) => {
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
		const items =
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
			items
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
					items,
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
		const items =
			$tagIds !== undefined && $selectionIds !== undefined
				? [...new Set([...$tagIds, ...$selectionIds])]
				: $tagIds !== undefined
				? $tagIds
				: $selectionIds;
		$model !== undefined &&
			metric !== undefined &&
			getHistogramMetrics(metadataHistograms, $model, metric, items, undefined).then((res) => {
				if (res === undefined) {
					return;
				}
				metadataHistograms = res;
			});
	});

	// Calculate histogram counts when model changes for postdistill columns
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
	<div id="metric-header" class="inline" style:margin-top="10px">
		<div class="inline">
			<h4>Metadata</h4>
			<div
				class="information-tooltip"
				use:tooltip={{
					content:
						'Interactive distributions for metadata columns. Click or drag on the histograms to filter the data. Add new metadata with @distill functions.',
					position: 'right',
					theme: 'zeno-tooltip'
				}}
			>
				<Icon style="outline:none" component={Svg} viewBox="-6 -6 36 36">
					<path d={mdiInformationOutline} />
				</Icon>
			</div>
			{#if $requestingHistogramCounts}
				<CircularProgress style="height: 15px; width: 15px; margin-left: 10px;" indeterminate />
			{/if}
		</div>
		<MetricRange />
	</div>
	{#each $columns.filter((m) => m.columnType === ZenoColumnType.LABEL) as col (columnHash(col))}
		<MetadataCell {col} histogram={metadataHistograms.get(col)} />
	{/each}
	{#each $columns.filter((m) => m.columnType === ZenoColumnType.PREDISTILL) as col (columnHash(col))}
		<MetadataCell {col} histogram={metadataHistograms.get(col)} />
	{/each}
	{#if $model}
		{#each $columns.filter((m) => m.columnType === ZenoColumnType.POSTDISTILL && m.model === $model) as col (columnHash(col))}
			<MetadataCell {col} histogram={metadataHistograms.get(col)} />
		{/each}
		{@const outputCol = $columns.filter(
			(m) => m.columnType === ZenoColumnType.OUTPUT && m.model === $model
		)}
		{#if outputCol.length > 0}
			<MetadataCell col={outputCol[0]} histogram={metadataHistograms.get(outputCol[0])} />
		{/if}
	{/if}
{/if}

<style>
	#metric-header {
		position: sticky;
		top: 110px;
		z-index: 2;
		border-bottom: 0.5px solid var(--G5);
		background-color: var(--Y2);
	}
	.inline {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
	.information-tooltip {
		width: 24px;
		height: 24px;
		cursor: help;
		fill: var(--G2);
	}
</style>
