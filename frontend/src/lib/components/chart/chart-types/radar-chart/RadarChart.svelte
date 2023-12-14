<script lang="ts">
	import type { Chart, RadarParameters } from '$lib/zenoapi';
	import { Vega, type VegaSpec } from 'svelte-vega';
	import generateSpec from './vegaSpec-radar';

	export let chart: Chart;
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
		spec = generateSpec(chart.parameters as RadarParameters, Math.min(width, height)) as VegaSpec;
	}
</script>

<Vega
	{spec}
	{data}
	options={{
		actions: { source: false, editor: false, compiled: false },
		width: Math.min(width, height),
		height: Math.min(width, height),
		scaleFactor: {
			png: 3
		},
		renderer: 'svg',
		theme: 'vox',
		downloadFileName: chart.name
	}}
/>
