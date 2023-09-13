<script lang="ts">
	import type { Chart, XCParameters } from '$lib/zenoapi';
	import { VegaLite } from 'svelte-vega';
	import generateSpec from './vegaSpec-bar';

	export let chart: Chart;
	export let data: { table: Record<string, unknown> };
	export let height = 500;
	export let width = 1000;

	$: parameters = chart.parameters as XCParameters;
	$: spec = generateSpec(parameters, height, width);
</script>

<VegaLite
	{spec}
	{data}
	options={{
		actions: { source: false, editor: false, compiled: false },
		width: width,
		height: height,
		scaleFactor: {
			png: 3
		}
	}}
/>
