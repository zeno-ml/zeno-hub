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
	{#await zenoClient.getChartData(chart.projectUuid, chart.id) then data}
		<div class="text-center">
			<svelte:component
				this={chartMap[chart.type]}
				{chart}
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
</div>
