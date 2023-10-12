<script lang="ts">
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
		ZenoService,
		type FilterPredicateGroup,
		type GroupMetric,
		type Metric,
		type MetricKey,
		type Slice
	} from '$lib/zenoapi';
	import { getContext, onMount } from 'svelte';
	import SelectionBar from '../metadata/SelectionBar.svelte';
	import ComparisonView from './ComparisonView.svelte';
	import ListView from './ListView.svelte';
	import TableView from './TableView.svelte';
	import { optionsMap } from './views/viewMap';

	export let compare: boolean;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let selected = 'list';
	let currentResult: Promise<GroupMetric[] | undefined> = new Promise(() => undefined);
	let modelAResult: Promise<GroupMetric[] | undefined> = new Promise(() => undefined);
	let modelBResult: Promise<GroupMetric[] | undefined> = new Promise(() => undefined);
	let numberOfInstances = 0;
	let viewOptions: Record<string, unknown> | undefined = undefined;

	$: secureTagIds = $tagIds === undefined ? [] : $tagIds;
	$: secureSelectionIds = $selectionIds === undefined ? [] : $selectionIds;

	// change selected to table if a tag is edited
	$: selected = $editTag !== undefined ? 'table' : selected;
	$: currentResult = zenoClient.getMetricsForSlices($project.uuid, {
		metricKeys: getMetricKeys($model, $metric, $selectionPredicates),
		dataIds: [...new Set([...secureTagIds, ...secureSelectionIds])]
	});

	$: modelAResult = compare
		? getCompareResults($model, $metric, $selectionPredicates)
		: new Promise(() => undefined);
	$: modelBResult = compare
		? getCompareResults($comparisonModel, $metric, $selectionPredicates)
		: new Promise(() => undefined);

	onMount(() => {
		if ($project.view === '') {
			selected = 'table';
		}
	});

	function getMetricKeys(
		model: string | undefined,
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
				model: model === undefined ? '' : model,
				metric: metric ? metric.id : -1
			}
		];
	}

	async function getCompareResults(
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
		return zenoClient.getMetricsForSlices($project.uuid, {
			metricKeys: getMetricKeys(model, metric, predicates),
			dataIds
		});
	}

	$: currentResult.then((d) => {
		if (d !== undefined && d.length > 0) {
			numberOfInstances = d[0].size;
		}
	});
</script>

<div class="flex justify-between align-center">
	<SelectionBar bind:selected {currentResult}>
		{#if optionsMap[$project.view] !== undefined}
			<svelte:component this={optionsMap[$project.view]} bind:viewOptions />
		{/if}
	</SelectionBar>
</div>
{#if compare && $metric && $model}
	{#if $comparisonModel !== undefined}
		<ComparisonView {modelAResult} {modelBResult} {viewOptions} />
	{/if}
{:else if $editTag !== undefined}
	<TableView {numberOfInstances} {viewOptions} />
{:else}
	{#if selected === 'list'}
		<ListView {numberOfInstances} {viewOptions} />
	{/if}
	{#if selected === 'table'}
		<TableView {numberOfInstances} {viewOptions} />
	{/if}
{/if}
