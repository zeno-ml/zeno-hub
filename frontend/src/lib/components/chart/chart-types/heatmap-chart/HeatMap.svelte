<script lang="ts">
	import type { Chart, ChartConfig, HeatmapParameters, Metric, ZenoService } from '$lib/zenoapi';
	import { getContext } from 'svelte';
	import { VegaLite, type VegaLiteSpec } from 'svelte-vega';
	import { getConfig } from '../../config';
	import generateSpec from './vegaSpec-heatmap';

	export let chart: Chart;
	export let chartConfig: ChartConfig;
	export let preview: boolean;
	export let data: {
		table: Array<{
			x_value: string | number;
			y_value: string | number;
			fixed_value: number;
			size: number;
		}>;
	};

	const zenoClient = getContext('zenoClient') as ZenoService;

	let spec: VegaLiteSpec;
	let metrics: Metric[] = [];
	zenoClient.getMetrics(chart.projectUuid).then((m) => (metrics = m));

	$: parameters = chart.parameters as HeatmapParameters;
	$: sliceVsSlice = parameters.xChannel === parameters.yChannel;
	$: {
		data;
		updateSpec();
	}

	function updateSpec() {
		const metric = metrics.find((m) => m.id === parameters.metric);
		if (metric) {
			spec = generateSpec(parameters, metric.name, preview);
		} else {
			spec = generateSpec(parameters, 'slice size', preview);
		}
	}
</script>

{#if sliceVsSlice}
	<h4>{parameters.model}</h4>
{/if}
<VegaLite
	{spec}
	{data}
	options={{
		actions: preview ? false : { source: false, editor: false, compiled: false },
		scaleFactor: {
			png: 3
		},
		width: 700,
		height: 700,
		renderer: 'svg',
		theme: 'vox',
		downloadFileName: chart.name,
		config: getConfig(chartConfig)
	}}
/>
