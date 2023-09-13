<script lang="ts">
	import BarChart from '$lib/components/chart/chart-types/bar-chart/BarChart.svelte';
	import { ChartType, ZenoService, type Chart, type ReportElement } from '$lib/zenoapi';
	import type { ComponentType } from 'svelte';
	import BeeswarmChart from '../chart/chart-types/beeswarm-chart/BeeswarmChart.svelte';
	import HeatMap from '../chart/chart-types/heatmap-chart/HeatMap.svelte';
	import LineChart from '../chart/chart-types/line-chart/LineChart.svelte';
	import RadarChart from '../chart/chart-types/radar-chart/RadarChart.svelte';
	import Table from '../chart/chart-types/table/Table.svelte';

	// import BarChartReport from '../report/bar-chart/BarChartReport.svelte';
	// import BeeswarmChartReport from '../report/beeswarm-chart/BeeswarmChartReport.svelte';
	// import HeatMapReport from '../report/heatmap-chart/HeatMapReport.svelte';
	// import LineChartReport from '../report/line-chart/LineChartReport.svelte';
	// import RadarChartReport from '../report/radar-chart/RadarChartReport.svelte';
	// import TableReportTable from '../report/table-report/TableReportTable.svelte';
	// import type { ReportChartElement } from '../util/demoMetadata';
	// import { ChartType } from '../zenoservice';

	// const ChartMap = {
	// 	[ChartType.BAR]: BarChartReport,
	// 	[ChartType.LINE]: LineChartReport,
	// 	[ChartType.TABLE]: TableReportTable,
	// 	[ChartType.BEESWARM]: BeeswarmChartReport,
	// 	[ChartType.RADAR]: RadarChartReport,
	// 	[ChartType.HEATMAP]: HeatMapReport
	// };

	const chartMap: Record<string, ComponentType> = {
		[ChartType.BAR]: BarChart,
		[ChartType.LINE]: LineChart,
		[ChartType.TABLE]: Table,
		[ChartType.BEESWARM]: BeeswarmChart,
		[ChartType.RADAR]: RadarChart,
		[ChartType.HEATMAP]: HeatMap
	};

	// export let element: ReportChartElement;
	export let element: ReportElement;
	export let chart: Chart;

	$: chartData = chart.projectUuid ? ZenoService.getChartData(chart.projectUuid, chart.id) : '';
</script>

{#await chartData}
	<p>Loading...</p>
{:then data}
	<svelte:component this={chartMap[chart.type]} {chart} data={JSON.parse(data)} />
{/await}
<!-- <ChartContainer chartName={chart.name}>
	<svelte:component this={chartMap[chart.type]} {chart} data={chartData} />
</ChartContainer> -->
<!-- 
<svelte:component this={ChartMap[element.type]} passedReport={$reports[element.reportIndex]} /> -->
