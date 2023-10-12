<script lang="ts">
	import BarChart from '$lib/components/chart/chart-types/bar-chart/BarChart.svelte';
	import BeeswarmChart from '$lib/components/chart/chart-types/beeswarm-chart/BeeswarmChart.svelte';
	import HeatMap from '$lib/components/chart/chart-types/heatmap-chart/HeatMap.svelte';
	import LineChart from '$lib/components/chart/chart-types/line-chart/LineChart.svelte';
	import RadarChart from '$lib/components/chart/chart-types/radar-chart/RadarChart.svelte';
	import Table from '$lib/components/chart/chart-types/table/Table.svelte';
	import { ChartType, type Chart, type ZenoService } from '$lib/zenoapi';
	import { getContext, type ComponentType } from 'svelte';

	const zenoClient = getContext('zenoClient') as ZenoService;

	const chartMap: Record<string, ComponentType> = {
		[ChartType.BAR]: BarChart,
		[ChartType.LINE]: LineChart,
		[ChartType.TABLE]: Table,
		[ChartType.BEESWARM]: BeeswarmChart,
		[ChartType.RADAR]: RadarChart,
		[ChartType.HEATMAP]: HeatMap
	};

	export let chart: Chart;
	export let width: number;

	$: chartData = zenoClient.getChartData(chart.projectUuid, chart.id);
</script>

{#await chartData}
	<p>Loading...</p>
{:then data}
	<div class="w-full">
		<h3 class="text-lg font-semibold">{chart.name}</h3>
		<div>
			<svelte:component
				this={chartMap[chart.type]}
				{chart}
				{width}
				data={JSON.parse(data)}
				height={chart.type == ChartType.RADAR ? 550 : 300}
			/>
		</div>
	</div>
{/await}
