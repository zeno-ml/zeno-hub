<script lang="ts">
	import { metrics, slices } from '$lib/stores';
	import { SlicesMetricsOrModels, type Chart, type RadarParameters } from '$lib/zenoapi';
	import { Vega } from 'svelte-vega';
	import generateSpec from './vegaSpec-radar';

	export let chart: Chart;
	export let data: {
		table: Array<{
			axis_value: string | number;
			fixed_value: number;
			layer_value: string | number;
			size: number;
		}>;
	};
	export let width = 700;
	export let height = 600;

	$: parameters = chart.parameters as RadarParameters;

	function getFixedName(): string {
		switch (parameters.fixedChannel) {
			case SlicesMetricsOrModels.SLICES:
				return $slices.find((sli) => sli.id === parameters.slices[0])?.sliceName ?? '';
			case SlicesMetricsOrModels.METRICS:
				return $metrics.find((met) => met.id === parameters.metrics[0])?.name ?? '';
			case SlicesMetricsOrModels.MODELS:
				return parameters.models[0];
		}
	}
</script>

<h4 class="m-0">{getFixedName()}</h4>
<Vega
	spec={generateSpec(parameters, width, height)}
	{data}
	options={{
		actions: { source: false, editor: false, compiled: false },
		width: width,
		height: height,
		scaleFactor: {
			png: 3
		}
	}}
/>
