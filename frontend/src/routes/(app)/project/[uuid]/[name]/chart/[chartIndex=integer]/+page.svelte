<script lang="ts">
	import { browser } from '$app/environment';
	import { page } from '$app/stores';
	import ChartContainer from '$lib/components/chart/ChartContainer.svelte';
	import EditHeader from '$lib/components/chart/chart-page/chart-header/EditHeader.svelte';
	import ViewHeader from '$lib/components/chart/chart-page/chart-header/ViewHeader.svelte';
	import Encoding from '$lib/components/chart/chart-page/encoding/Encoding.svelte';
	import ViewSelection from '$lib/components/chart/chart-page/view-selection/ViewSelection.svelte';
	import { project } from '$lib/stores';
	import { chartMap } from '$lib/util/charts';
	import type { Chart, ZenoService } from '$lib/zenoapi';
	import { getContext, onMount } from 'svelte';

	export let data;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let mounted = false;
	let isChartEdit: boolean | undefined;
	let chart = data.chart;
	let updatingData = false;
	let chartDataRequest = zenoClient.getChartData(chart.projectUuid, chart.id);

	$: updateEditUrl(isChartEdit);
	$: updateChart(chart);

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
		updatingData = true;
		if (mounted && $project && $project.editor && browser) {
			zenoClient.updateChart($project.uuid, chart).then(() => {
				chartDataRequest = zenoClient.getChartData(chart.projectUuid, chart.id);
				updatingData = false;
			});
		} else {
			updatingData = false;
		}
	}

	// Prevent calling updateChart on mount
	onMount(() => {
		mounted = true;
	});
</script>

<div class={`flex w-full overflow-hidden ${isChartEdit ? 'flex-row' : 'flex-col'}`}>
	{#if isChartEdit && $project.editor}
		<div
			class="h-full w-[380px] shrink-0 overflow-y-auto border-r border-r-grey-lighter bg-yellowish-light px-5 pb-20"
		>
			<EditHeader bind:isChartEdit bind:chart bind:chartConfig={data.chartConfig} />
			<ViewSelection bind:chart />
			<Encoding bind:chart />
		</div>
	{:else}
		<ViewHeader bind:isChartEdit />
	{/if}
	{#await chartDataRequest then chartData}
		<div class={`flex h-full w-full flex-col overflow-auto pl-2`}>
			<ChartContainer chartName={chart.name} loading={updatingData}>
				<svelte:component
					this={chartMap[chart.type]}
					{chart}
					data={JSON.parse(chartData)}
					width={900}
					chartConfig={data.chartConfig}
				/>
			</ChartContainer>
		</div>
	{:catch error}
		<p class="ml-4 mt-4 font-semibold text-error">
			Chart data could not be loaded: {error.message}
		</p>
	{/await}
</div>
