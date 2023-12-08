<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import ChartContainer from '$lib/components/chart/ChartContainer.svelte';
	import { metrics, models } from '$lib/stores';
	import { chartMap } from '$lib/util/charts.js';

	export let data;

	if ($models.length === 0 || $metrics.length === 0) {
		goto(`${$page.url.pathname}/explore`);
	}
</script>

{#if data.charts.length > 0 && data.charts[0]}
	{@const overviewChart = data.charts[0]}
	<ChartContainer chartName={overviewChart.name}>
		<svelte:component
			this={chartMap[overviewChart.type]}
			chart={overviewChart}
			data={overviewChart.data}
			width={900}
		/>
	</ChartContainer>
{/if}
