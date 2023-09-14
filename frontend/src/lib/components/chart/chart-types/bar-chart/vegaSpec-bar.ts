import { metrics } from '$lib/stores';
import { SlicesOrModels, type XCParameters } from '$lib/zenoapi';
import type { VegaLiteSpec } from 'svelte-vega';
import { get } from 'svelte/store';

export default function generateSpec(
	parameters: XCParameters,
	height: number,
	width: number
): VegaLiteSpec {
	const x_name = parameters.xChannel === SlicesOrModels.MODELS ? 'model' : 'slice';
	const color_name = parameters.colorChannel === SlicesOrModels.SLICES ? 'slice' : 'model';
	const metric = get(metrics).find((metric) => metric.id === parameters.metric);

	const spec = {
		$schema: 'https://vega.github.io/schema/vega-lite/v5.json',
		description: 'A simple bar chart with embedded data.',
		autosize: 'pad',
		width: width,
		height: height,
		data: {
			name: 'table'
		},
		encoding: {
			x: {
				title: x_name,
				field: 'x_value',
				type: 'nominal',
				axis: {
					labelAngle: 45,
					labelFontSize: 14,
					titleFontSize: 14,
					titlePadding: 10,
					labelExpr: 'datum.label'
				},
				sort: null
			},
			y: {
				title: metric?.name ?? '',
				field: 'y_value',
				type: 'quantitative',
				axis: {
					labelFontSize: 14,
					titleFontSize: 14,
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
						{ field: 'y_value', type: 'quantitative', title: metric?.name ?? '' },
						{ field: 'color_value', type: 'ordinal', title: color_name },
						{ field: 'size', type: 'quantitative' }
					]
				}
			},
			{
				mark: {
					type: 'text',
					style: 'label'
				},
				encoding: {
					text: {
						field: 'y_value',
						type: 'quantitative',
						format: '.2f'
					}
				}
			}
		],
		config: {
			style: { label: { align: 'center', dy: -5 } }
		}
	};

	return spec as VegaLiteSpec;
}
