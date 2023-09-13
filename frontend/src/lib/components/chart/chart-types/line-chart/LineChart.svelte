<script lang="ts">
	import type { Chart, XCParameters } from '$lib/zenoapi';
	import { VegaLite } from 'svelte-vega';
	import generateSpec from './vegaSpec-line';

	export let chart: Chart;
	export let data: { table: Record<string, unknown> };
	export let width = 1000;
	export let height = 400;

	$: parameters = chart.parameters as XCParameters;
</script>

<VegaLite
	spec={generateSpec(parameters, width, height)}
	{data}
	options={{
		actions: { source: false, editor: false, compiled: false },
		scaleFactor: {
			png: 3
		}
	}}
/>
