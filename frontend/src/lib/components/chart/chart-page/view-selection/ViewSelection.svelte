<script lang="ts">
	import { projectConfig } from '$lib/stores';
	import { ChartType, ZenoService, type Chart } from '$lib/zenoapi';
	import { chartDefaults } from '../../chartUtil';
	import ChartElement from './ChartElement.svelte';

	export let chart: Chart;
	export let chartData: { table: Record<string, unknown> } | undefined;

	async function updateChart(chartType: ChartType) {
		if (chart.type !== chartType && $projectConfig) {
			chart = { ...chartDefaults(chart.name, chart.id, chartType) };
			chartData = undefined;
			chartData = JSON.parse(await ZenoService.getChartData($projectConfig.uuid, chart));
		}
	}
</script>

<div class="mb-5">
	<h4 class="border-b-2 border-grey-light mb-2">Chart Type</h4>
	<div class="flex flex-wrap justify-between">
		<ChartElement {chart} {updateChart} type={ChartType.BAR} />
		<ChartElement {chart} {updateChart} type={ChartType.LINE} />
		<ChartElement {chart} {updateChart} type={ChartType.TABLE} />
		<ChartElement {chart} {updateChart} type={ChartType.BEESWARM} />
		<ChartElement {chart} {updateChart} type={ChartType.RADAR} />
		<ChartElement {chart} {updateChart} type={ChartType.HEATMAP} />
	</div>
</div>
