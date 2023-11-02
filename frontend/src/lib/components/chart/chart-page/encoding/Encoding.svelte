<script lang="ts">
	import { ChartType, type Chart } from '$lib/zenoapi';
	import type { ComponentType } from 'svelte';
	import BeeswarmEncoding from './chart-encoding/BeeswarmEncoding.svelte';
	import HeatmapEncoding from './chart-encoding/HeatmapEncoding.svelte';
	import RadarEncoding from './chart-encoding/RadarEncoding.svelte';
	import TableEncoding from './chart-encoding/TableEncoding.svelte';
	import XcChartEncoding from './chart-encoding/XCChartEncoding.svelte';

	export let chart: Chart;

	const encodingMap: Record<string, ComponentType> = {
		[ChartType.BAR]: XcChartEncoding,
		[ChartType.LINE]: XcChartEncoding,
		[ChartType.TABLE]: TableEncoding,
		[ChartType.BEESWARM]: BeeswarmEncoding,
		[ChartType.RADAR]: RadarEncoding,
		[ChartType.HEATMAP]: HeatmapEncoding
	};
</script>

<div class="mb-20">
	<h4 class="mb-2 border-b-2 border-grey-light pb-1">Encoding</h4>
	<div id="flex flex-col">
		<svelte:component this={encodingMap[chart.type]} bind:chart />
	</div>
</div>
