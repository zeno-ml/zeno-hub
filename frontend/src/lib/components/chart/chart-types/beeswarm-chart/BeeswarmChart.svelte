<script lang="ts">
	import { metrics, slices } from '$lib/stores';
	import { SlicesOrModels, type BeeswarmParameters, type Chart } from '$lib/zenoapi';
	import { Vega } from 'svelte-vega';
	import generateSpec from './vegaSpec-beeswarm';

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
			? parameters.metrics.map((id) => $metrics.find((metric) => metric.id === id)?.name ?? 'count')
			: parameters.yChannel === SlicesOrModels.MODELS
			? parameters.models
			: parameters.slices.map((id) => $slices.find((sli) => sli.id === id)?.sliceName ?? '');

	function dataFilter(
		data: {
			table: Array<{
				color_value: string | number;
				x_value: number;
				y_value: string | number;
				size: number;
				metric: number;
			}>;
		},
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
			table: data.table.filter(
				(element) => element.metric === metric && element.y_value === yCompare
			)
		};
	}
</script>

{#each rows as row}
	<h4 class="mb-2.5">
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
				? row
				: $metrics.find((met) => met.id === parameters.metrics[0])?.name ?? ''
		)}
		data={dataFilter(
			data,
			parameters.fixedDimension === 'y'
				? row
				: $metrics.find((metric) => metric.id === parameters.metrics[0])?.name,
			parameters.colorChannel === SlicesOrModels.MODELS
				? parameters.fixedDimension === 'y'
					? $slices.find((slice) => slice.id === parameters.slices[0])?.sliceName ?? ''
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
