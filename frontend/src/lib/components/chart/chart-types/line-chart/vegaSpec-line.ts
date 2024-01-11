import { SlicesOrModels, type XCParameters } from '$lib/zenoapi';
import type { VegaLiteSpec } from 'svelte-vega';

export default function generateSpec(
	parameters: XCParameters,
	metricName: string,
	width: number,
	height: number,
	preview: boolean
): VegaLiteSpec {
	const x_name = parameters.xChannel === SlicesOrModels.MODELS ? 'system' : 'slice';
	const color_name = parameters.colorChannel === SlicesOrModels.SLICES ? 'slice' : 'system';
	const legend = preview ? { disable: true } : {};
	const xAxis = preview ? false : { labelAngle: 45, titlePadding: 10 };

	return {
		$schema: 'https://vega.github.io/schema/vega-lite/v5.json',
		description: 'A simple line chart with embedded data.',
		random_id: Date.now(), // used to force re-rendering of the chart
		width: width,
		height: height,
		autosize: 'fit',
		padding: { top: 20, right: 10 },
		data: {
			name: 'table'
		},
		encoding: {
			x: {
				title: x_name,
				field: 'x_value',
				type: 'nominal',
				axis: xAxis,
				sort: null
			},
			y: {
				title: metricName,
				field: 'y_value',
				type: 'quantitative',
				axis: {
					titlePadding: 20
				},
				sort: null
			},
			color: {
				condition: {
					param: 'hover',
					field: 'color_value',
					scale: { scheme: 'category20' },
					sort: null,
					title: color_name
				},
				value: 'grey'
			},
			opacity: { condition: { param: 'hover', value: 1 }, value: 0.1 }
		},
		layer: [
			{
				params: [
					{
						name: 'hover',
						select: {
							type: 'point',
							fields: ['color_value'],
							on: 'mouseover'
						}
					}
				],
				mark: {
					type: 'circle',
					size: 100
				},
				encoding: {
					tooltip: [
						{ field: 'x_value', type: 'ordinal', title: x_name },
						{ field: 'y_value', type: 'quantitative', title: metricName, format: '.4f' },
						{ field: 'color_value', type: 'ordinal', title: color_name },
						{ field: 'size', type: 'quantitative' }
					]
				}
			},
			{
				params: [
					{
						name: 'hover_line',
						select: {
							type: 'point',
							fields: ['color_value'],
							on: 'mouseover'
						}
					}
				],
				mark: {
					type: 'line'
				}
			},
			{
				transform: [{ filter: { param: 'hover', empty: false } }],
				mark: {
					type: 'text',
					style: 'label'
				},
				encoding: {
					text: {
						field: 'y_value',
						type: 'quantitative',
						format: '.4f'
					},
					color: { value: 'black' }
				}
			}
		],
		config: {
			style: { label: { dy: -13, dx: -2 } },
			legend: legend
		}
	} as VegaLiteSpec;
}
