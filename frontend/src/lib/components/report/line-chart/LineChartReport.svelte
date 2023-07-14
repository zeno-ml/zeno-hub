<script lang="ts">
	import { VegaLite } from 'svelte-vega';
	import type { Chart } from '$lib/zenoapi';
	import generateSpec from './vegaSpec-line';

	export let chart: Chart;
	export let data: { table: Record<string, unknown> };
</script>

<div class="main">
	<div class="model-result">
		<VegaLite
			spec={generateSpec(chart.parameters)}
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
