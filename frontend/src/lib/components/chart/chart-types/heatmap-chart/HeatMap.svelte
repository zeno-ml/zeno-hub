<script lang="ts">
	import { ZenoService, type Chart, type HeatmapParameters } from '$lib/zenoapi';
	import { VegaLite, type VegaLiteSpec } from 'svelte-vega';
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

	let spec: VegaLiteSpec;

	$: parameters = chart.parameters as HeatmapParameters;
	$: sliceVsSlice = parameters.xChannel === parameters.yChannel;
	$: ZenoService.getMetrics(chart.projectUuid).then((metrics) => {
		const metric = metrics.find((m) => m.id === parameters.metric);
		if (metric) {
			spec = generateSpec(parameters, metric.name);
		} else {
			spec = generateSpec(parameters, 'slice size');
		}
	});
</script>

{#if sliceVsSlice}
	<h4>{parameters.model}</h4>
{/if}
<VegaLite
	{spec}
	{data}
	options={{
		actions: { source: false, editor: false, compiled: false },
		scaleFactor: {
			png: 3
		},
		width: 700,
		height: 700,
		renderer: 'svg',
		theme: 'vox'
	}}
/>
