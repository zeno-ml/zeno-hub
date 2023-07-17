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

<div class={isChartEdit ? 'row-flex chart-panel' : 'col-flex chart-panel'}>
	{#if isChartEdit}
		<div class="edit-bar">
			<EditHeader bind:isChartEdit bind:chart {updateChart} />
			<ViewSelection bind:chart bind:chartData />
			<Encoding bind:chart />
		</div>
	{:else}
		<ViewHeader bind:isChartEdit {chart} />
	{/if}
	{#if chartData}
		<div class={isChartEdit ? 'edit-charts charts' : 'charts'}>
			<svelte:component this={chartMap[chart.type]} {chart} data={chartData} />
		</div>
	{/if}
</div>

<style>
	.chart-panel {
		width: 100%;
		display: flex;
		overflow: hidden;
	}

	.row-flex {
		flex-direction: row;
	}

	.col-flex {
		flex-direction: column;
	}

	.edit-bar {
		height: calc(100vh - 15px);
		width: 370px;
		min-width: 370px;
		max-width: 370px;
		padding-top: 10px;
		padding-bottom: 0px;
		padding-left: 15px;
		padding-right: 15px;
		overflow-y: scroll;
		background-color: var(--Y2);
	}

	.charts {
		height: calc(100vh - 15px);
		overflow: auto;
		display: flex;
		flex-direction: column;
		padding-top: 10px;
		padding-left: 15px;
	}

	.edit-charts {
		width: 100%;
	}
</style>
