<script lang="ts">
	import { chartMap } from '$lib/util/charts';
	import { ChartType, ZenoService, type Chart } from '$lib/zenoapi';
	import { getContext } from 'svelte';

	export let chart: Chart;
	export let width: number;

	const zenoClient = getContext('zenoClient') as ZenoService;
</script>

<div class="w-full">
	{#if chart === undefined}
		<p class="ml-4 mt-4 font-semibold text-error">Chart does not exist anymore.</p>
	{:else}
		<h3 class="text-lg font-semibold">{chart.name}</h3>
		{#await zenoClient.getChartConfig(chart.projectUuid, chart.id) then chartConfig}
			{#await zenoClient.getChartData(chart.projectUuid, chart.id) then data}
				<div class="text-center">
					<svelte:component
						this={chartMap[chart.type]}
						{chart}
						{chartConfig}
						{width}
						data={JSON.parse(data)}
						height={chart.type == ChartType.RADAR ? 600 : 400}
					/>
				</div>
			{:catch error}
				<p class="ml-4 mt-4 font-semibold text-error">
					Chart data could not be loaded: {error.message}
				</p>
			{/await}
		{:catch error}
			<p class="ml-4 mt-4 font-semibold text-error">
				Chart config could not be loaded: {error.message}
			</p>
		{/await}
	{/if}
</div>
