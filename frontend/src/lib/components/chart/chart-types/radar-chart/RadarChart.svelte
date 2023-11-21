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
	export let height = 575;
	export let width: number;

	let spec: VegaSpec;

	$: {
		data;
		updateSpec();
	}

	function updateSpec() {
		spec = generateSpec(
			chart.parameters as RadarParameters,
			Math.min(height, width),
			Math.min(height, width)
		) as VegaSpec;
	}
</script>

<Vega
	{spec}
	{data}
	options={{
		actions: { source: false, editor: false, compiled: false },
		width: Math.min(height, width),
		height: Math.min(height, width),
		scaleFactor: {
			png: 3
		},
		renderer: 'svg',
		theme: 'vox',
		downloadFileName: chart.name
	}}
/>
