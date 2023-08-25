<script lang="ts">
	import { ChartType, type Chart } from '$lib/zenoapi';
	import type { ComponentType } from 'svelte';
	import BarChartIcon from './chart-icons/BarChartIcon.svelte';
	import BeeswarmIcon from './chart-icons/BeeswarmIcon.svelte';
	import HeatMapIcon from './chart-icons/HeatMapIcon.svelte';
	import LineChartIcon from './chart-icons/LineChartIcon.svelte';
	import RadarChartIcon from './chart-icons/RadarChartIcon.svelte';
	import TableIcon from './chart-icons/TableIcon.svelte';

	export let chart: Chart;
	export let updateChart: (chartType: ChartType) => void;
	export let type: ChartType;

	const iconMap: Record<string, ComponentType> = {
		[ChartType.BAR]: BarChartIcon,
		[ChartType.LINE]: LineChartIcon,
		[ChartType.TABLE]: TableIcon,
		[ChartType.BEESWARM]: BeeswarmIcon,
		[ChartType.RADAR]: RadarChartIcon,
		[ChartType.HEATMAP]: HeatMapIcon
	};

	const titleMap: Record<string, string> = {
		[ChartType.BAR]: 'Bar Chart',
		[ChartType.LINE]: 'Line Chart',
		[ChartType.TABLE]: 'Table',
		[ChartType.BEESWARM]: 'Beeswarm',
		[ChartType.RADAR]: 'Radar Chart',
		[ChartType.HEATMAP]: 'Heatmap'
	};
</script>

<div
	class="flex flex-col border-2 border-grey-light rounded-lg bg-background h-20 w-[105px] items-center p-2 m-1 hover:bg-primary-light cursor-pointer {chart.type ===
	type
		? 'bg-primary-light'
		: ''}"
	on:keydown={() => ({})}
	on:click={() => updateChart(type)}
>
	<svelte:component this={iconMap[type]} />
	<h4 class="mt-1">{titleMap[type]}</h4>
</div>
