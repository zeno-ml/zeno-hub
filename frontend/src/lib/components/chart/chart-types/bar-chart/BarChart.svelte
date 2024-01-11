<script lang="ts">
	import type { Chart, ChartConfig, Metric, XCParameters, ZenoService } from '$lib/zenoapi';
	import { getContext } from 'svelte';
	import { VegaLite, type VegaLiteSpec } from 'svelte-vega';
	import { getConfig } from '../../config';
	import generateSpec from './vegaSpec-bar';

	export let chart: Chart;
	export let chartConfig: ChartConfig;
	export let data: { table: Record<string, unknown> };
	export let height = 400;
	export let width: number;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let spec: VegaLiteSpec;
	let metrics: Metric[] = [];
	zenoClient.getMetrics(chart.projectUuid).then((m) => (metrics = m));

	$: {
		data;
		updateChart(metrics);
	}

	function updateChart(mets: Metric[]) {
		const params = chart.parameters as XCParameters;
		const metric = mets.find((m) => m.id === params.metric);
		if (metric) {
			spec = generateSpec(params, metric.name, height, width);
		} else {
			spec = generateSpec(params, 'slice size', height, width);
		}
	}
</script>

<VegaLite
	{spec}
	{data}
	options={{
		actions: { source: false, editor: false, compiled: false },
		height: height,
		width: width,
		scaleFactor: {
			png: 3
		},
		renderer: 'svg',
		theme: 'vox',
		downloadFileName: chart.name,
		config: getConfig(chartConfig)
	}}
/>
