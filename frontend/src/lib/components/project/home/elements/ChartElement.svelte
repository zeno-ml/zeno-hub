<script lang="ts">
	import { chartMap } from '$lib/util/charts';
	import type { Chart, ZenoService } from '$lib/zenoapi';
	import { getContext } from 'svelte';

	export let chart: Chart;
	export let width: number;
	export let height: number;

	const zenoClient = getContext('zenoClient') as ZenoService;
</script>

<h3 class="mb-4 font-semibold text-grey-dark">{chart.name}</h3>
{#await zenoClient.getChartConfig(chart.projectUuid, chart.id) then chartConfig}
	{#await zenoClient.getChartData(chart.projectUuid, chart.id) then data}
		<svelte:component
			this={chartMap[chart.type]}
			class="flex overflow-auto"
			{chart}
			{width}
			{height}
			{chartConfig}
			data={JSON.parse(data)}
		/>
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
