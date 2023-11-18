<script lang="ts">
	import SelectionBar from '$lib/components/metadata/SelectionBar.svelte';
	import {
		comparisonModel,
		filterSelection,
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
	import ComparisonView from './ComparisonView.svelte';
	import ListView from './ListView.svelte';
	import TableView from './TableView.svelte';

	export let compare: boolean;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let selected = 'list';
	let currentResult: GroupMetric[] | undefined;
	let modelAResult: Promise<GroupMetric[] | undefined> = new Promise(() => undefined);
	let modelBResult: Promise<GroupMetric[] | undefined> = new Promise(() => undefined);
	let numberOfInstances = 0;

	$: secureIds = [
		...($tagIds === undefined ? [] : $tagIds),
		...($filterSelection ? $selectionIds : [])
	];
	$: zenoClient
		.getMetricsFiltered($project.uuid, {
			metricKeys: getMetricKeys($model, $metric, $selectionPredicates),
			dataIds: [...new Set(secureIds)]
		})
		.then((r) => {
			currentResult = r;
			if (r !== undefined && r.length > 0) {
				numberOfInstances = r[0].size;
			}
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
		const secureIds = [
			...($tagIds === undefined ? [] : $tagIds),
			...($filterSelection ? $selectionIds : [])
		];
		const dataIds = [...new Set(secureIds)];
		return zenoClient.getMetricsFiltered($project.uuid, {
			metricKeys: getMetricKeys(model, metric, predicates),
			dataIds
		});
	}
</script>

<SelectionBar {currentResult} bind:selected />
{#if compare && $metric && $model}
	{#if $comparisonModel !== undefined}
		<ComparisonView {modelAResult} {modelBResult} />
	{/if}
{:else}
	{#if selected === 'list'}
		<ListView {numberOfInstances} />
	{/if}
	{#if selected === 'table'}
		<TableView {numberOfInstances} />
	{/if}
{/if}
