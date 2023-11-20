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
	export let updateChartType: (chartType: ChartType) => void;
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

<button
	class="flex h-20 cursor-pointer flex-col items-center rounded-lg border-2 border-grey-light bg-background p-2 hover:bg-primary-light {chart.type ===
	type
		? 'bg-primary-light'
		: ''}"
	on:click={() => updateChartType(type)}
>
	<svelte:component this={iconMap[type]} />
	<h4 class="mt-1">{titleMap[type]}</h4>
</button>
