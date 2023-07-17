<script lang="ts">
	import type { Chart, XCParameters } from '$lib/zenoapi';
	import { VegaLite } from 'svelte-vega';
	import generateSpec from './vegaSpec-bar';

	export let chart: Chart;
	export let data: { table: Record<string, unknown> };

	$: parameters = chart.parameters as XCParameters;
	$: spec = generateSpec(parameters);
</script>

<div class="main">
	<div class="model-result">
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
	</div>
</div>

<style>
	.main {
		margin-left: 20px;
	}
	.model-result {
		margin-top: 30px;
	}
</style>
