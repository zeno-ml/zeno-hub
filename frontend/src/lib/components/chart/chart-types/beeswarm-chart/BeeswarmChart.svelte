<script lang="ts">
	import {
		SlicesOrModels,
		ZenoService,
		type BeeswarmParameters,
		type Chart,
		type ChartConfig,
		type Metric,
		type Slice
	} from '$lib/zenoapi';
	import { extent } from 'd3-array';
	import { getContext } from 'svelte';
	import { Vega } from 'svelte-vega';
	import { getConfig } from '../../config';
	import generateSpec from './vegaSpec-beeswarm';

	export let chart: Chart;
	export let chartConfig: ChartConfig;
	export let data: {
		table: Array<{
			color_value: string | number;
			x_value: number;
			y_value: string | number;
			size: number;
			metric: number;
		}>;
	};
	export let width: number;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let range: [number, number] = [0, 0];
	let metrics: Metric[] = [];
	let slices: Slice[] = [];

	zenoClient.getMetrics(chart.projectUuid).then((met) => {
		metrics = met;
	});
	zenoClient.getSlices(chart.projectUuid).then((sli) => {
		slices = sli;
	});

	$: {
		let ext = extent(data.table, (d) => d.x_value);
		if (ext[0] !== undefined && ext[1] !== undefined) {
			range = [ext[0] as number, ext[1] as number];
		}
	}
	$: parameters = chart.parameters as BeeswarmParameters;
	$: rows =
		parameters.fixedDimension === 'y'
			? parameters.metrics.map((id) => metrics.find((metric) => metric.id === id)?.name ?? 'count')
			: parameters.yChannel === SlicesOrModels.MODELS
				? parameters.models
				: parameters.slices.map((id) => slices.find((sli) => sli.id === id)?.sliceName ?? '');

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

{#each rows as row, i}
	<div class="h-40 text-left">
		<h4 class="relative mb-2.5 text-lg">
			{parameters.fixedDimension === 'y'
				? parameters.yChannel === SlicesOrModels.MODELS
					? parameters.models[0]
					: slices.find((sli) => sli.id === parameters.slices[0])?.sliceName
				: row}
		</h4>
		<Vega
			spec={generateSpec(
				parameters,
				parameters.fixedDimension === 'y'
					? row
					: metrics.find((met) => met.id === parameters.metrics[0])?.name ?? '',
				range,
				i === 0,
				width
			)}
			data={dataFilter(
				data,
				parameters.fixedDimension === 'y'
					? row
					: metrics.find((metric) => metric.id === parameters.metrics[0])?.name,
				parameters.colorChannel === SlicesOrModels.MODELS
					? parameters.fixedDimension === 'y'
						? slices.find((slice) => slice.id === parameters.slices[0])?.sliceName ?? ''
						: row
					: undefined,
				parameters.colorChannel === SlicesOrModels.SLICES
					? parameters.fixedDimension === 'y'
						? parameters.models[0]
						: row
					: undefined
			)}
			options={{
				actions: false,
				width: width - 200,
				height: 80,
				scaleFactor: {
					png: 3
				},
				renderer: 'svg',
				theme: 'vox',
				downloadFileName: chart.name,
				config: getConfig(chartConfig)
			}}
		/>
	</div>
{/each}
