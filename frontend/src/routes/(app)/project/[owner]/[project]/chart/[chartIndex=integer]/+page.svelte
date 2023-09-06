<script lang="ts">
	import { browser } from '$app/environment';
	import { invalidateAll } from '$app/navigation';
	import { page } from '$app/stores';
	import ChartContainer from '$lib/components/chart/ChartContainer.svelte';
	import EditHeader from '$lib/components/chart/chart-page/chart-header/EditHeader.svelte';
	import ViewHeader from '$lib/components/chart/chart-page/chart-header/ViewHeader.svelte';
	import Encoding from '$lib/components/chart/chart-page/encoding/Encoding.svelte';
	import ViewSelection from '$lib/components/chart/chart-page/view-selection/ViewSelection.svelte';
	import { chartMap } from '$lib/components/chart/chartUtil.js';
	import { charts, project } from '$lib/stores.js';
	import { ZenoService, type Chart } from '$lib/zenoapi';
	import { overrideItemIdKeyNameBeforeInitialisingDndZones } from 'svelte-dnd-action';

	export let data;

	let isChartEdit: boolean | undefined;
	let chart = data.chart;
	let chartData: { table: Record<string, unknown> } | undefined = data.chartData;

	$: updateEditUrl(isChartEdit);
	$: reloadData(chart);
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
		if ($project) {
			ZenoService.updateChart($project.uuid, chart).then(() => {
				invalidateAll();
				charts.update((c) => {
					let index = c.findIndex((c) => c.id === chart.id);
					if (index !== -1) {
						c[index] = chart;
					}
					return c;
				});
			});
		}
	}

	async function reloadData(chart: Chart) {
		if ($project && browser) {
			chartData = JSON.parse(await ZenoService.getChartData($project.uuid, chart));
		}
	}
</script>

<div class={`w-full flex overflow-hidden ${isChartEdit ? 'flex-row' : 'flex-col'}`}>
	{#if isChartEdit && $project?.editor}
		<div class="h-full pb-20 px-5 overflow-y-auto shrink-0 bg-yellowish-light w-[380px]">
			<EditHeader bind:isChartEdit bind:chart />
			<ViewSelection bind:chart bind:chartData />
			<Encoding bind:chart />
		</div>
	{:else}
		<ViewHeader bind:isChartEdit />
	{/if}
	{#if chartData}
		<div class={`overflow-auto flex flex-col pl-2 h-full ${isChartEdit ? 'w-full' : ''}`}>
			<ChartContainer chartName={chart.name}>
				<svelte:component this={chartMap[chart.type]} {chart} data={chartData} />
			</ChartContainer>
		</div>
	{/if}
</div>
