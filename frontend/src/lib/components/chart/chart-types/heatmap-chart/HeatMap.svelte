<script lang="ts">
	import type { Chart, HeatmapParameters } from '$lib/zenoapi';
	import { VegaLite } from 'svelte-vega';
	import generateSpec from './vegaSpec-heatmap';

	export let chart: Chart;
	export let data: {
		table: Array<{
			x_value: string | number;
			y_value: string | number;
			fixed_value: number;
			size: number;
		}>;
	};

	$: parameters = chart.parameters as HeatmapParameters;
	$: sliceVsSlice = parameters.xChannel === parameters.yChannel;
</script>

<div class="main">
	<div class="model-result">
		{#if sliceVsSlice}
			<h4>{parameters.model}</h4>
		{/if}
		<VegaLite
			spec={generateSpec(parameters)}
			{data}
			options={{
				actions: { source: false, editor: false, compiled: false },
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
