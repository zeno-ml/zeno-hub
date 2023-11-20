<script lang="ts">
	import { chartDefaults } from '$lib/util/charts';
	import { ChartType, type Chart } from '$lib/zenoapi';
	import ChartElement from './ChartElement.svelte';

	export let chart: Chart;

	async function updateChartType(chartType: ChartType) {
		if (chart.type !== chartType) {
			chart = chartDefaults(chart.name, chart.id, chart.projectUuid, chartType);
		}
	}
</script>

<div class="mb-5">
	<h4 class="mb-2 border-b-2 border-grey-light pb-1">Chart Type</h4>
	<div class="grid grid-cols-3 gap-2">
		<ChartElement {chart} {updateChartType} type={ChartType.BAR} />
		<ChartElement {chart} {updateChartType} type={ChartType.LINE} />
		<ChartElement {chart} {updateChartType} type={ChartType.TABLE} />
		<ChartElement {chart} {updateChartType} type={ChartType.BEESWARM} />
		<ChartElement {chart} {updateChartType} type={ChartType.RADAR} />
		<ChartElement {chart} {updateChartType} type={ChartType.HEATMAP} />
	</div>
</div>
