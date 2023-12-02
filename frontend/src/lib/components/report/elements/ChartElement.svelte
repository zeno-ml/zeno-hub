<script lang="ts">
	import { chartMap } from '$lib/util/charts';
	import { ChartType, type Chart } from '$lib/zenoapi';

	export let chart: Chart;
	export let width: number;
</script>

<div class="w-full">
	<h3 class="text-lg font-semibold">{chart.name}</h3>
	<div>
		<svelte:component
			this={chartMap[chart.type]}
			{chart}
			{width}
			data={JSON.parse(chart.data || '{}')}
			height={chart.type == ChartType.RADAR ? 600 : 400}
		/>
	</div>
</div>
