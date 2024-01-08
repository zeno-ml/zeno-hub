import { SlicesOrModels, type HeatmapParameters } from '$lib/zenoapi';
import type { VegaLiteSpec } from 'svelte-vega';

export default function generateSpec(
	parameters: HeatmapParameters,
	metricName: string,
	preview: boolean
): VegaLiteSpec {
	const x_name = parameters.xChannel === SlicesOrModels.MODELS ? 'system' : 'slice';
	const y_name = parameters.yChannel === SlicesOrModels.SLICES ? 'slice' : 'system';

	return {
		$schema: 'https://vega.github.io/schema/vega-lite/v5.json',
		random_id: Date.now(), // used to force re-rendering of the chart
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
				axis: preview
					? false
					: {
							labelAngle: -20,
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
				mark: { type: 'text' },
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
			},
			legend: preview ? { disable: true } : {}
		}
	} as VegaLiteSpec;
}
