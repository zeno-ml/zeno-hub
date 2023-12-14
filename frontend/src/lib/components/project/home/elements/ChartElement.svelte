<script lang="ts">
	import { chartMap } from '$lib/util/charts';
	import type { Chart } from '$lib/zenoapi';

	export let chart: Chart;
	export let width: number;
	export let height: number;
</script>

<h3 class="mb-2 text-lg font-semibold">{chart.name}</h3>
{#if chart.data}
	<svelte:component
		this={chartMap[chart.type]}
		class="flex overflow-auto"
		{chart}
		{width}
		{height}
		data={JSON.parse(chart.data)}
	/>
{/if}
