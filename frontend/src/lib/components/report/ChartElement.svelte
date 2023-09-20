<script lang="ts">
	import BarChart from '$lib/components/chart/chart-types/bar-chart/BarChart.svelte';
	import { ChartType, ZenoService, type Chart } from '$lib/zenoapi';
	import type { ComponentType } from 'svelte';
	import BeeswarmChart from '../chart/chart-types/beeswarm-chart/BeeswarmChart.svelte';
	import HeatMap from '../chart/chart-types/heatmap-chart/HeatMap.svelte';
	import LineChart from '../chart/chart-types/line-chart/LineChart.svelte';
	import RadarChart from '../chart/chart-types/radar-chart/RadarChart.svelte';
	import Table from '../chart/chart-types/table/Table.svelte';

	const chartMap: Record<string, ComponentType> = {
		[ChartType.BAR]: BarChart,
		[ChartType.LINE]: LineChart,
		[ChartType.TABLE]: Table,
		[ChartType.BEESWARM]: BeeswarmChart,
		[ChartType.RADAR]: RadarChart,
		[ChartType.HEATMAP]: HeatMap
	};

	export let chart: Chart;

	$: chartData = ZenoService.getChartData(chart.projectUuid, chart.id);
</script>

{#await chartData}
	<p>Loading...</p>
{:then data}
	<h3 class="text-lg font-semibold">{chart.name}</h3>
	<div>
		<svelte:component
			this={chartMap[chart.type]}
			{chart}
			data={JSON.parse(data)}
			width={650}
			height={chart.type == ChartType.RADAR ? 550 : 300}
		/>
	</div>
{/await}
