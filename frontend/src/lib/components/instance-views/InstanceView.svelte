<script lang="ts">
	import { getMetricsForSlicesAndTags } from '$lib/api/slice';
	import {
		comparisonModel,
		editTag,
		metric,
		model,
		projectConfig,
		selectionIds,
		selectionPredicates,
		tagIds
	} from '$lib/stores';
	import {
		Join,
		type FilterPredicateGroup,
		type Metric,
		type MetricKey,
		type Slice
	} from '$lib/zenoapi';
	import { onMount } from 'svelte';
	import SelectionBar from '../metadata/SelectionBar.svelte';
	import ComparisonView from './ComparisonView.svelte';
	import ListView from './ListView.svelte';
	import TableView from './TableView.svelte';
	import { optionsMap } from './views/viewMap';

	export let compare: boolean;

	let selected = 'list';
	let viewOptions: Record<string, unknown> | undefined = undefined;

	$: secureTagIds = $tagIds === undefined ? [] : $tagIds;
	$: secureSelectionIds = $selectionIds === undefined ? [] : $selectionIds;

	onMount(() => {
		if ($projectConfig === undefined || $projectConfig.view === '') {
			selected = 'table';
			return;
		}
	});

	function getMetricKeys(
		model: string,
		metric: Metric,
		predicates?: FilterPredicateGroup
	): MetricKey[] {
		return [
			<MetricKey>{
				slice: <Slice>{
					id: 0,
					sliceName: '',
					folderId: undefined,
					filterPredicates: {
						predicates: predicates !== undefined ? [predicates] : [],
						join: Join._
					}
				},
				model: model,
				metric: metric
			}
		];
	}

	function getCompareResults(model: string, metric: Metric, predicates?: FilterPredicateGroup) {
		const secureTagIds = $tagIds === undefined ? [] : $tagIds;
		const secureSelectionIds = $selectionIds === undefined ? [] : $selectionIds;
		const items = [...new Set([...secureTagIds, ...secureSelectionIds])];
		return getMetricsForSlicesAndTags(getMetricKeys(model, metric, predicates), items, true);
	}

	// change selected to table if a tag is edited
	$: selected = $editTag !== undefined ? 'table' : selected;
</script>

{#if $model && $metric}
	{@const metricKeys = getMetricKeys($model, $metric, $selectionPredicates)}
	{#await getMetricsForSlicesAndTags(metricKeys, [...new Set( [...secureTagIds, ...secureSelectionIds] )], false) then currentResult}
		<div class="heading">
			<SelectionBar bind:selected {currentResult}>
				{#if $projectConfig !== undefined && optionsMap[$projectConfig.view] !== undefined}
					<svelte:component this={optionsMap[$projectConfig.view]} bind:viewOptions />
				{/if}
			</SelectionBar>
		</div>
		{#if compare}
			{#if $comparisonModel !== undefined}
				{#await getCompareResults($model, $metric, $selectionPredicates) then modelAResult}
					{#await getCompareResults($comparisonModel, $metric, $selectionPredicates) then modelBResult}
						<ComparisonView {modelAResult} {modelBResult} {viewOptions} />
					{/await}
				{/await}
			{/if}
		{:else if $editTag !== undefined}
			<TableView {currentResult} {viewOptions} />
		{:else}
			{#if selected === 'list'}
				<ListView {currentResult} {viewOptions} />
			{/if}
			{#if selected === 'table'}
				<TableView {currentResult} {viewOptions} />
			{/if}
		{/if}
	{/await}
{/if}

<style>
	.heading {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
	}
</style>
