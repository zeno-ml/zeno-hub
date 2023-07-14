<script lang="ts">
	import Beeswarm from './chart-icons/BeeswarmIcon.svelte';
	import BarChart from './chart-icons/BarChartIcon.svelte';
	import LineChart from './chart-icons/LineChartIcon.svelte';
	import Table from './chart-icons/TableIcon.svelte';
	import Radar from './chart-icons/RadarChartIcon.svelte';
	import HeatMap from './chart-icons/HeatMapIcon.svelte';

	import { ChartType, type Chart, ZenoService } from '$lib/zenoapi';
	import { chartDefaults } from '../../reportUtil';
	import { currentProject } from '$lib/stores';

	export let chart: Chart;
	export let chartData: { table: Record<string, unknown> } | undefined;

	async function updateChart(chartType: ChartType) {
		if (chart.type !== chartType && $currentProject) {
			chart = { ...chartDefaults(chart.name, chart.id, chartType) };
			chartData = undefined;
			chartData = JSON.parse(await ZenoService.getChartData($currentProject.uuid, chart));
		}
	}
</script>

<div class="chart-type">
	<h4 class="edit-title">Chart Type</h4>
	<div class="chart-flex">
		<div
			class="chart-element {chart.type === ChartType.BAR ? 'selected' : ''}"
			on:keydown={() => ({})}
			on:click={() => updateChart(ChartType.BAR)}
		>
			<BarChart />
			<h4 class="chart-title">Bar Chart</h4>
		</div>
		<div
			class="chart-element {chart.type === ChartType.LINE ? 'selected' : ''}"
			on:keydown={() => ({})}
			on:click={() => updateChart(ChartType.LINE)}
		>
			<LineChart />
			<h4 class="chart-title">Line Chart</h4>
		</div>
		<div
			class="chart-element {chart.type === ChartType.TABLE ? 'selected' : ''}"
			on:keydown={() => ({})}
			on:click={() => updateChart(ChartType.TABLE)}
		>
			<Table />
			<h4 class="chart-title">Table</h4>
		</div>
		<div
			class="chart-element {chart.type === ChartType.BEESWARM ? 'selected' : ''}"
			on:keydown={() => ({})}
			on:click={() => updateChart(ChartType.BEESWARM)}
		>
			<Beeswarm />
			<h4 class="chart-title">Beeswarm</h4>
		</div>
		<div
			class="chart-element {chart.type === ChartType.RADAR ? 'selected' : ''}"
			on:keydown={() => ({})}
			on:click={() => updateChart(ChartType.RADAR)}
		>
			<Radar />
			<h4 class="chart-title">Radar Chart</h4>
		</div>
		<div
			class="chart-element {chart.type === ChartType.HEATMAP ? 'selected' : ''}"
			on:keydown={() => ({})}
			on:click={() => updateChart(ChartType.HEATMAP)}
		>
			<HeatMap />
			<h4 class="chart-title">Heat Map</h4>
		</div>
	</div>
</div>

<style>
	.chart-type {
		margin-bottom: 20px;
	}
	.edit-title {
		border-bottom: 1px solid var(--G4);
	}
	.chart-flex {
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		justify-content: space-between;
	}
	.chart-element {
		display: flex;
		flex-direction: column;
		border: 1px solid var(--G4);
		background: white;
		height: 60px;
		width: 90px;
		border-radius: 10px;
		align-items: center;
		padding: 10px;
		margin: 2px;
	}
	.chart-element:hover {
		cursor: pointer;
		background: var(--P3);
	}
	.selected {
		background: var(--P3);
	}
	.chart-title {
		margin: 5px 0px 0px 0px;
		font-weight: 500;
	}
</style>
