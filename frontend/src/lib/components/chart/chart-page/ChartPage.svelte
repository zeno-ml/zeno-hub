<script lang="ts">
	import type { Chart } from '$lib/zenoapi';
	import { onMount } from 'svelte';
	import { overrideItemIdKeyNameBeforeInitialisingDndZones } from 'svelte-dnd-action';
	import { chartMap } from '../chartUtil';
	import EditHeader from './chart-header/EditHeader.svelte';
	import ViewHeader from './chart-header/ViewHeader.svelte';
	import Encoding from './encoding/Encoding.svelte';
	import ViewSelection from './view-selection/ViewSelection.svelte';

	export let params: {
		chart: Chart;
		chartData: { table: Record<string, unknown> };
		chartIndex: number;
	};
	let isChartEdit = false;

	overrideItemIdKeyNameBeforeInitialisingDndZones('value');

	onMount(() => {
		if (window.location.href.split('/').slice(-2, -1)[0] === 'new') {
			isChartEdit = true;
		}
	});
</script>

<div id="chart-panel" class={isChartEdit ? 'row-flex' : 'col-flex'}>
	{#if isChartEdit}
		<div id="edit-bar">
			<EditHeader bind:isChartEdit chart={params.chart} />
			<ViewSelection chart={params.chart} chartData={params.chartData} />
			<Encoding chart={params.chart} />
		</div>
	{:else}
		<ViewHeader bind:isChartEdit chart={params.chart} />
	{/if}
	<div id="charts" class={isChartEdit ? 'edit-charts' : ''}>
		<svelte:component
			this={chartMap[params.chart.type]}
			chart={params.chart}
			data={params.chartData}
		/>
	</div>
</div>

<style>
	#chart-panel {
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
	#edit-bar {
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
	#charts {
		height: calc(100vh - 15px);
		overflow: scroll;
		display: flex;
		flex-direction: column;
		padding-top: 10px;
		padding-left: 15px;
	}
	.edit-charts {
		width: 100%;
	}
</style>
