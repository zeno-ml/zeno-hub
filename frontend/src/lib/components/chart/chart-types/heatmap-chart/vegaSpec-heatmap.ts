import { SlicesOrModels, type HeatmapParameters } from '$lib/zenoapi';
import type { VegaLiteSpec } from 'svelte-vega';

export default function generateSpec(
	parameters: HeatmapParameters,
	metricName: string
): VegaLiteSpec {
	const x_name = parameters.xChannel === SlicesOrModels.MODELS ? 'model' : 'slice';
	const y_name = parameters.yChannel === SlicesOrModels.SLICES ? 'slice' : 'model';

	return {
		$schema: 'https://vega.github.io/schema/vega-lite/v5.json',
		autosize: 'fit',
		data: {
			name: 'table'
		},
		transform: [
			{
				joinaggregate: [
					{
						op: 'average',
						field: 'fixed_value',
						as: 'mean_value'
					}
				]
			}
		],
		encoding: {
			x: {
				title: x_name,
				field: 'x_value',
				type: 'ordinal',
				axis: {
					labelAngle: -20,
					labelFontSize: 14,
					titleFontSize: 14,
					orient: 'top',
					titlePadding: 10
				},
				sort: null
			},
			y: {
				title: y_name,
				field: 'y_value',
				type: 'ordinal',
				axis: {
					labelFontSize: 14,
					titleFontSize: 14,
					titlePadding: 10
				},
				sort: null
			}
		},
		layer: [
			{
				params: [
					{
						name: 'hover',
						select: {
							type: 'point',
							field: 'fixed_value',
							on: 'mouseover'
						}
					}
				],
				mark: {
					type: 'rect'
				},
				encoding: {
					tooltip: [
						{ field: 'x_value', type: 'ordinal', title: x_name },
						{ field: 'y_value', type: 'ordinal', title: y_name },
						{ field: 'fixed_value', type: 'quantitative', title: metricName },
						{ field: 'size', type: 'quantitative' }
					],
					color: {
						title: metricName,
						field: 'fixed_value',
						type: 'quantitative',
						scale: { scheme: 'purples' }
					},
					fillOpacity: {
						condition: [
							{
								param: 'hover',
								empty: false,
								value: 1
							}
						],
						value: 0.7
					}
				}
			},
			{
				mark: { type: 'text', fontSize: 12 },
				encoding: {
					text: {
						field: 'fixed_value',
						type: 'quantitative',
						format: '.2f'
					},
					color: {
						condition: {
							test: 'datum.fixed_value < datum.mean_value',
							value: 'black'
						},
						value: 'white'
					}
				}
			}
		],
		config: {
			rect: { cornerRadius: 5 },
			axis: { ticks: false, labelPadding: 15, domain: false },
			view: {
				strokeWidth: 0,
				step: 70
			}
		}
	} as VegaLiteSpec;
}
