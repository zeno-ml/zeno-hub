<script lang="ts">
	import type { Chart, XCParameters } from '$lib/zenoapi';
	import { VegaLite } from 'svelte-vega';
	import generateSpec from './vegaSpec-line';

	export let chart: Chart;
	export let data: { table: Record<string, unknown> };

	$: parameters = chart.parameters as XCParameters;
</script>

<VegaLite
	spec={generateSpec(parameters)}
	{data}
	options={{
		actions: { source: false, editor: false, compiled: false },
		width: 1000,
		height: 400,
		scaleFactor: {
			png: 3
		}
	}}
/>
