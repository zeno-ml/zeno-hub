<script lang="ts">
	import { ZenoService, type Chart, type XCParameters } from '$lib/zenoapi';
	import { VegaLite, type VegaLiteSpec } from 'svelte-vega';
	import generateSpec from './vegaSpec-bar';

	export let chart: Chart;
	export let data: { table: Record<string, unknown> };
	export let height = 400;
	export let width: number;

	let spec: VegaLiteSpec;

	$: parameters = chart.parameters as XCParameters;
	$: ZenoService.getMetrics(chart.projectUuid).then((metrics) => {
		const metric = metrics.find((m) => m.id === parameters.metric);
		if (metric) {
			spec = generateSpec(parameters, metric.name, height, width);
		} else {
			spec = generateSpec(parameters, 'slice size', height, width);
		}
	});
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
		theme: 'vox'
	}}
/>
