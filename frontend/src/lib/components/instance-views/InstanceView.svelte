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
		type GroupMetric,
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
	let currentResult: GroupMetric[] | undefined = undefined;
	let viewOptions: Record<string, unknown> | undefined = undefined;
	let modelAResult: GroupMetric[] | undefined = undefined;
	let modelBResult: GroupMetric[] | undefined = undefined;

	$: secureTagIds = $tagIds === undefined ? [] : $tagIds;
	$: secureSelectionIds = $selectionIds === undefined ? [] : $selectionIds;

	// change selected to table if a tag is edited
	$: selected = $editTag !== undefined ? 'table' : selected;
	$: if ($model) {
		getMetricsForSlicesAndTags($model ? getMetricKeys($model, $metric, $selectionPredicates) : [], [
			...new Set([...secureTagIds, ...secureSelectionIds])
		]).then((res) => (currentResult = res));
	}

	$: getCompareResults($model, $metric, $selectionPredicates).then((r) => (modelAResult = r));
	$: getCompareResults($comparisonModel, $metric, $selectionPredicates).then(
		(r) => (modelBResult = r)
	);

	onMount(() => {
		if ($project === undefined || $project.view === '') {
			selected = 'table';
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
				metric: metric ? metric.id : -1
			}
		];
	}

	function getCompareResults(
		model: string | undefined,
		metric: Metric | undefined,
		predicates?: FilterPredicateGroup
	) {
		if (model === undefined || metric === undefined) {
			return Promise.resolve(undefined);
		}
		const secureTagIds = $tagIds === undefined ? [] : $tagIds;
		const secureSelectionIds = $selectionIds === undefined ? [] : $selectionIds;
		const dataIds = [...new Set([...secureTagIds, ...secureSelectionIds])];
		return getMetricsForSlicesAndTags(getMetricKeys(model, metric, predicates), dataIds);
	}
</script>

<div class="flex justify-between align-center">
	<SelectionBar bind:selected {currentResult}>
		{#if $project !== undefined && optionsMap[$project.view] !== undefined}
			<svelte:component this={optionsMap[$project.view]} bind:viewOptions />
		{/if}
	</SelectionBar>
</div>
{#if compare && $metric && $model}
	{#if $comparisonModel !== undefined}
		<ComparisonView {modelAResult} {modelBResult} {viewOptions} />
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
