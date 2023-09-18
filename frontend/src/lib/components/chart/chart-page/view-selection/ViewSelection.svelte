<script lang="ts">
	import { project } from '$lib/stores';
	import { chartDefaults } from '$lib/util/charts';
	import { ChartType, type Chart } from '$lib/zenoapi';
	import ChartElement from './ChartElement.svelte';

	export let chart: Chart;

	async function updateChart(chartType: ChartType) {
		if (chart.type !== chartType && $project) {
			chart = chartDefaults(chart.name, chart.id, chart.projectUuid, chartType);
		}
	}
</script>

<div class="mb-5">
	<h4 class="border-b-2 border-grey-light mb-2 pb-1">Chart Type</h4>
	<div class="flex flex-wrap justify-between">
		<ChartElement {chart} {updateChart} type={ChartType.BAR} />
		<ChartElement {chart} {updateChart} type={ChartType.LINE} />
		<ChartElement {chart} {updateChart} type={ChartType.TABLE} />
		<ChartElement {chart} {updateChart} type={ChartType.BEESWARM} />
		<ChartElement {chart} {updateChart} type={ChartType.RADAR} />
		<ChartElement {chart} {updateChart} type={ChartType.HEATMAP} />
	</div>
</div>
