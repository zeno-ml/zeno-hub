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

<div id="encoding">
	<h4 class="edit-type">Encoding</h4>
	<div id="encoding-flex">
		<svelte:component this={encodingMap[chart.type]} bind:chart />
	</div>
</div>

<style>
	.edit-type {
		border-bottom: 1px solid var(--G4);
	}
	#encoding {
		margin-bottom: 50px;
	}
	#encoding-flex {
		display: flex;
		flex-direction: column;
		margin-bottom: 80px;
	}
</style>
