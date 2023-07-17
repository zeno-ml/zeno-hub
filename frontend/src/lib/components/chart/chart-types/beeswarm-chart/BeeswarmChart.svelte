<script lang="ts">
	import { Vega } from 'svelte-vega';
	import generateSpec from './vegaSpec-beeswarm';
	import { type Chart, type BeeswarmParameters, SlicesOrModels } from '$lib/zenoapi';
	import { slices, metrics } from '$lib/stores';

	export let chart: Chart;
	export let data: {
		table: Array<{
			color_value: string | number;
			x_value: number;
			y_value: string | number;
			size: number;
			metric: number;
		}>;
	};

	$: parameters = chart.parameters as BeeswarmParameters;
	$: rows =
		parameters.fixedDimension === 'y'
			? parameters.metrics
			: parameters.yChannel === SlicesOrModels.MODELS
			? parameters.models
			: parameters.slices.map((id) => $slices.find((sli) => sli.id === id)?.sliceName);

	function dataFilter(
		metric: number | string | undefined,
		slice: string | number | undefined,
		model: string | number | undefined
	): {
		table: Array<{
			color_value: string | number;
			x_value: number;
			y_value: string | number;
			size: number;
			metric: number;
		}>;
	} {
		const yCompare = parameters.yChannel === SlicesOrModels.MODELS ? model : slice;
		return {
			...data,
			table: data.table.filter(
				(element) => element.metric === metric && element.y_value === yCompare
			)
		};
	}
</script>

<div class="main">
	<div class="model-result">
		{#each rows as row}
			<h4>
				{parameters.fixedDimension === 'y'
					? parameters.yChannel === SlicesOrModels.MODELS
						? parameters.models[0]
						: $slices.find((sli) => sli.id === parameters.slices[0])?.sliceName
					: row}
			</h4>
			<Vega
				spec={generateSpec(
					parameters,
					parameters.fixedDimension === 'y'
						? $metrics.find((met) => met.id === row)?.name ?? ''
						: $metrics.find((met) => met.id === parameters.metrics[0])?.name ?? ''
				)}
				data={dataFilter(
					parameters.fixedDimension === 'y' ? row : parameters.metrics[0],
					parameters.colorChannel === SlicesOrModels.MODELS
						? parameters.fixedDimension === 'y'
							? parameters.slices[0]
							: row
						: undefined,
					parameters.colorChannel === SlicesOrModels.SLICES
						? parameters.fixedDimension === 'y'
							? parameters.models[0]
							: row
						: undefined
				)}
				options={{
					actions: { source: false, editor: false, compiled: false },
					width: 800,
					height: 100,
					scaleFactor: {
						png: 3
					}
				}}
			/>
		{/each}
	</div>
</div>

<style>
	.main {
		margin-left: 20px;
	}
	.model-result {
		margin-top: 30px;
	}
	.model-result h4 {
		margin: 0px 0px 10px 0px;
	}
</style>
