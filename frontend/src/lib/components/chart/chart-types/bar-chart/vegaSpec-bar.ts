import { SlicesOrModels, type XCParameters } from '$lib/zenoapi';
import type { VegaLiteSpec } from 'svelte-vega';

export default function generateSpec(
	parameters: XCParameters,
	metricName: string,
	height: number,
	width: number,
	preview: boolean
): VegaLiteSpec {
	const x_name = parameters.xChannel === SlicesOrModels.MODELS ? 'system' : 'slice';
	const color_name = parameters.colorChannel === SlicesOrModels.SLICES ? 'slice' : 'system';

	const spec = {
		$schema: 'https://vega.github.io/schema/vega-lite/v5.json',
		description: 'A simple bar chart with embedded data.',
		random_id: Date.now(), // used to force re-rendering of the chart
		height: height,
		width: width,
		autosize: 'fit',
		data: {
			name: 'table'
		},
		encoding: {
			x: {
				title: x_name,
				field: 'x_value',
				type: 'nominal',
				axis: preview
					? false
					: {
							labelAngle: 45,
							titlePadding: 10,
							labelExpr: 'datum.label'
					  },
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
			xOffset: {
				field: 'color_value',
				sort: null
			},
			fillOpacity: {
				condition: { param: 'highlight', value: 1, empty: false },
				value: 0.8
			}
		},
		layer: [
			{
				params: [
					{
						name: 'highlight',
						select: {
							type: 'point',
							field: 'y_value',
							on: 'mouseover'
						}
					}
				],
				mark: {
					type: 'bar'
				},
				encoding: {
					color: {
						field: 'color_value',
						sort: null,
						scale: { scheme: 'category20' },
						title: color_name
					},
					tooltip: [
						{ field: 'x_value', type: 'ordinal', title: x_name },
						{ field: 'y_value', type: 'quantitative', title: metricName, format: '.4f' },
						{ field: 'color_value', type: 'ordinal', title: color_name },
						{ field: 'size', type: 'quantitative' }
					]
				}
			}
		],
		config: {
			style: { label: { align: 'center', dy: -5 } },
			legend: preview ? { disable: true } : {}
		}
	};

	return spec as VegaLiteSpec;
}
