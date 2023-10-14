<script lang="ts">
	import { browser } from '$app/environment';
	import { invalidate } from '$app/navigation';
	import { page } from '$app/stores';
	import ChartContainer from '$lib/components/chart/ChartContainer.svelte';
	import EditHeader from '$lib/components/chart/chart-page/chart-header/EditHeader.svelte';
	import ViewHeader from '$lib/components/chart/chart-page/chart-header/ViewHeader.svelte';
	import Encoding from '$lib/components/chart/chart-page/encoding/Encoding.svelte';
	import ViewSelection from '$lib/components/chart/chart-page/view-selection/ViewSelection.svelte';
	import { project } from '$lib/stores';
	import { chartMap } from '$lib/util/charts';
	import type { Chart, ZenoService } from '$lib/zenoapi';
	import { getContext } from 'svelte';
	import { overrideItemIdKeyNameBeforeInitialisingDndZones } from 'svelte-dnd-action';

	export let data;

	const zenoClient = getContext('zenoClient') as ZenoService;
	let isChartEdit: boolean | undefined;
	let chart = data.chart;
	let chartData: { table: Record<string, unknown> } | undefined;
	let unique = {};

	$: chartData = data.chartData;
	$: updateEditUrl(isChartEdit);
	$: updateChart(chart);

	overrideItemIdKeyNameBeforeInitialisingDndZones('value');

	function updateEditUrl(edit: boolean | undefined) {
		if (edit === undefined) {
			let param = $page.url.searchParams.get('edit');
			isChartEdit = param !== null && param === 'true' ? true : false;
			return;
		}
		$page.url.searchParams.set('edit', edit ? 'true' : 'false');
		if (browser) {
			window.history.replaceState({}, '', $page.url.toString());
		}
	}

	function updateChart(chart: Chart) {
		if ($project && $project.editor && browser) {
			zenoClient.updateChart($project.uuid, chart).then(() => {
				invalidate('app:chart');
			});
		}
	}
</script>

<div class={`w-full flex overflow-hidden ${isChartEdit ? 'flex-row' : 'flex-col'}`}>
	{#if isChartEdit && $project.editor}
		<div
			class="border-r border-r-grey-lighter h-full pb-20 px-5 overflow-y-auto shrink-0 bg-yellowish-light w-[380px]"
		>
			<EditHeader bind:isChartEdit bind:chart />
			<ViewSelection bind:chart bind:unique />
			<!--
				This is a hack to force the component to rerender on chart type change as the selections otherwise don't update.
				If svelecte ever resolves this issue, this hack can be removed and we can listen to events on svelecte.
				https://github.com/mskocik/svelecte/issues/200.
				A detailed description of this problem is in: https://github.com/zeno-ml/zeno-hub/pull/235.
			-->
			{#key unique}
				<Encoding bind:chart />
			{/key}
		</div>
	{:else}
		<ViewHeader bind:isChartEdit />
	{/if}
	{#if chartData}
		<div class={`overflow-auto flex flex-col pl-2 h-full`}>
			<ChartContainer chartName={chart.name}>
				<svelte:component this={chartMap[chart.type]} {chart} data={chartData} width={900} />
			</ChartContainer>
		</div>
	{/if}
</div>
