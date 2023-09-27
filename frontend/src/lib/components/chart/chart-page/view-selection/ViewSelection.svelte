<script lang="ts">
	import { chartDefaults } from '$lib/util/charts';
	import { ChartType, type Chart } from '$lib/zenoapi';
	import ChartElement from './ChartElement.svelte';

	export let chart: Chart;
	export let unique: unknown;

	async function updateChartType(chartType: ChartType) {
		if (chart.type !== chartType) {
			chart = chartDefaults(chart.name, chart.id, chart.projectUuid, chartType);
			unique = {};
		}
	}
</script>

<div class="mb-5">
	<h4 class="border-b-2 border-grey-light mb-2 pb-1">Chart Type</h4>
	<div class="flex flex-wrap justify-between">
		<ChartElement {chart} {updateChartType} type={ChartType.BAR} />
		<ChartElement {chart} {updateChartType} type={ChartType.LINE} />
		<ChartElement {chart} {updateChartType} type={ChartType.TABLE} />
		<ChartElement {chart} {updateChartType} type={ChartType.BEESWARM} />
		<ChartElement {chart} {updateChartType} type={ChartType.RADAR} />
		<ChartElement {chart} {updateChartType} type={ChartType.HEATMAP} />
	</div>
</div>
