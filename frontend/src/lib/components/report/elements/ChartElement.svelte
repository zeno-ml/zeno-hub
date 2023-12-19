<script lang="ts">
	import { chartMap } from '$lib/util/charts';
	import { ChartType, type Chart, type ChartConfig } from '$lib/zenoapi';

	export let chart: Chart;
	export let chartConfig: ChartConfig;
	export let width: number;
</script>

<div class="w-full">
	<h3 class="text-lg font-semibold">{chart.name}</h3>
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
</div>
