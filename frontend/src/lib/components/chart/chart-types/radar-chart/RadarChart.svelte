<script lang="ts">
	import type { Chart, ChartConfig, RadarParameters } from '$lib/zenoapi';
	import { Vega, type VegaSpec } from 'svelte-vega';
	import { getConfig } from '../../config';
	import generateSpec from './vegaSpec-radar';

	export let chart: Chart;
	export let chartConfig: ChartConfig;
	export let preview: boolean;
	export let data: {
		table: Array<{
			axis_value: string | number;
			fixed_value: number;
			layer_value: string | number;
			size: number;
		}>;
	};
	export let height = 600;
	export let width = 600;

	let spec: VegaSpec;

	$: {
		data;
		width;
		height;
		updateSpec();
	}

	function updateSpec() {
		spec = generateSpec(
			chart.parameters as RadarParameters,
			Math.min(width, height),
			preview
		) as VegaSpec;
	}
</script>

<Vega
	{spec}
	{data}
	options={{
		actions: preview ? false : { source: false, editor: false, compiled: false },
		width: Math.min(width, height),
		height: Math.min(width, height),
		scaleFactor: {
			png: 3
		},
		renderer: 'svg',
		theme: 'vox',
		downloadFileName: chart.name,
		config: getConfig(chartConfig)
	}}
/>
