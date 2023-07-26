<script lang="ts">
	import { browser } from '$app/environment';
	import EditHeader from '$lib/components/chart/chart-page/chart-header/EditHeader.svelte';
	import ViewHeader from '$lib/components/chart/chart-page/chart-header/ViewHeader.svelte';
	import Encoding from '$lib/components/chart/chart-page/encoding/Encoding.svelte';
	import ViewSelection from '$lib/components/chart/chart-page/view-selection/ViewSelection.svelte';
	import { chartMap } from '$lib/components/chart/chartUtil.js';
	import { charts, projectConfig } from '$lib/stores.js';
	import { ZenoService, type Chart } from '$lib/zenoapi';
	import { overrideItemIdKeyNameBeforeInitialisingDndZones } from 'svelte-dnd-action';

	export let data;

	let isChartEdit = false;
	let chart = data.chart;
	let chartData: { table: Record<string, unknown> } | undefined = data.chartData;

	$: reloadData(chart);

	overrideItemIdKeyNameBeforeInitialisingDndZones('value');

	function updateChart() {
		if ($projectConfig) {
			ZenoService.updateChart($projectConfig.uuid, chart).then(() => {
				if ($projectConfig)
					ZenoService.getCharts($projectConfig.uuid).then((fetchedCharts) =>
						charts.set(fetchedCharts)
					);
			});
		}
	}

	async function reloadData(chart: Chart) {
		if ($projectConfig && browser) {
			chartData = JSON.parse(await ZenoService.getChartData($projectConfig.uuid, chart));
		}
	}
</script>

<div class={`w-full flex overflow-hidden ${isChartEdit ? 'flex-row' : 'flex-col'}`}>
	{#if isChartEdit}
		<div class="h-full pt-5 pb-20 px-5 overflow-y-auto shrink-0 bg-yellowish-light w-96">
			<EditHeader bind:isChartEdit bind:chart {updateChart} />
			<ViewSelection bind:chart bind:chartData />
			<Encoding bind:chart />
		</div>
	{:else}
		<ViewHeader bind:isChartEdit {chart} />
	{/if}
	{#if chartData}
		<div class={`overflow-auto flex flex-col pt-3 pl-2 ${isChartEdit ? 'w-full' : ''}`}>
			<svelte:component this={chartMap[chart.type]} {chart} data={chartData} />
		</div>
	{/if}
</div>
