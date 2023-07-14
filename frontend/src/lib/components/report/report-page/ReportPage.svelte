<script lang="ts">
	import type { Chart } from '$lib/zenoapi';
	import { onMount } from 'svelte';
	import { overrideItemIdKeyNameBeforeInitialisingDndZones } from 'svelte-dnd-action';
	import { chartMap } from '../reportUtil';
	import Encoding from './encoding/Encoding.svelte';
	import EditHeader from './report-header/EditHeader.svelte';
	import ViewHeader from './report-header/ViewHeader.svelte';
	import ViewSelection from './view-selection/ViewSelection.svelte';

	export let params: {
		chart: Chart;
		chartData: { table: Record<string, unknown> };
		reportIndex: number;
	};
	let isReportEdit = false;

	overrideItemIdKeyNameBeforeInitialisingDndZones('value');

	onMount(() => {
		if (window.location.href.split('/').slice(-2, -1)[0] === 'new') {
			isReportEdit = true;
		}
	});
</script>

<div id="report-panel" class={isReportEdit ? 'row-flex' : 'col-flex'}>
	{#if isReportEdit}
		<div id="edit-bar">
			<EditHeader bind:isReportEdit chart={params.chart} />
			<ViewSelection chart={params.chart} chartData={params.chartData} />
			<Encoding chart={params.chart} />
		</div>
	{:else}
		<ViewHeader bind:isReportEdit chart={params.chart} />
	{/if}
	<div id="reports" class={isReportEdit ? 'edit-reports' : ''}>
		<svelte:component
			this={chartMap[params.chart.type]}
			chart={params.chart}
			data={params.chartData}
		/>
	</div>
</div>

<style>
	#report-panel {
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
	#reports {
		height: calc(100vh - 15px);
		overflow: scroll;
		display: flex;
		flex-direction: column;
		padding-top: 10px;
		padding-left: 15px;
	}
	.edit-reports {
		width: 100%;
	}
</style>
