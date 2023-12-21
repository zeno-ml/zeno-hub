<script lang="ts">
	import { chartMap } from '$lib/util/charts';
	import { ChartType, ZenoService, type Chart } from '$lib/zenoapi';
	import { getContext } from 'svelte';

	export let chart: Chart;
	export let width: number;

	const zenoClient = getContext('zenoClient') as ZenoService;
</script>

<div class="w-full">
	<h3 class="text-lg font-semibold">{chart.name}</h3>
	{#await zenoClient.getChartConfig(chart.projectUuid, chart.id) then chartConfig}
		{#if chart.data}
			<div class="text-center">
				<svelte:component
					this={chartMap[chart.type]}
					{chart}
					{chartConfig}
					{width}
					data={JSON.parse(chart.data)}
					height={chart.type == ChartType.RADAR ? 600 : 400}
				/>
			</div>
		{/if}
	{/await}
</div>
