<script lang="ts">
	import type { Chart, XCParameters } from '$lib/zenoapi';
	import { VegaLite } from 'svelte-vega';
	import generateSpec from './vegaSpec-bar';

	export let chart: Chart;
	export let data: { table: Record<string, unknown> };

	$: parameters = chart.parameters as XCParameters;
	$: spec = generateSpec(parameters);
</script>

<VegaLite
	{spec}
	{data}
	options={{
		actions: { source: false, editor: false, compiled: false },
		width: 1000,
		height: 500,
		scaleFactor: {
			png: 3
		}
	}}
/>
