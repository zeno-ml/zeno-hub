<script lang="ts">
	import { getMetricsForSlicesAndTags } from '$lib/api/slice';
	import {
		comparisonModel,
		editTag,
		metric,
		model,
		project,
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
		if ($project === undefined || $project.view === '') {
			selected = 'table';
			return;
		}
	});

	function getMetricKeys(
		model: string,
		metric: Metric | undefined,
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
				metric: metric ?? {
					id: -1,
					name: 'count'
				}
			}
		];
	}

	function getCompareResults(model: string, metric: Metric, predicates?: FilterPredicateGroup) {
		const secureTagIds = $tagIds === undefined ? [] : $tagIds;
		const secureSelectionIds = $selectionIds === undefined ? [] : $selectionIds;
		const dataIds = [...new Set([...secureTagIds, ...secureSelectionIds])];
		return getMetricsForSlicesAndTags(getMetricKeys(model, metric, predicates), dataIds, true);
	}

	// change selected to table if a tag is edited
	$: selected = $editTag !== undefined ? 'table' : selected;
</script>

{#if $model}
	{#await getMetricsForSlicesAndTags(getMetricKeys($model, $metric, $selectionPredicates), [...new Set( [...secureTagIds, ...secureSelectionIds] )], false) then currentResult}
		<div class="flex justify-between align-center">
			<SelectionBar bind:selected {currentResult}>
				{#if $project !== undefined && optionsMap[$project.view] !== undefined}
					<svelte:component this={optionsMap[$project.view]} bind:viewOptions />
				{/if}
			</SelectionBar>
		</div>
		{#if compare && $metric}
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
