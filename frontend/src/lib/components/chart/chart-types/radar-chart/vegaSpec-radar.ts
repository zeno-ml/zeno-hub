import { SlicesOrModels, type RadarParameters } from '$lib/zenoapi';
import type { VisualizationSpec } from 'vega-embed';

export default function generateSpec(
	parameters: RadarParameters,
	width: number,
	height: number
): VisualizationSpec {
	const spec = {
		$schema: 'https://vega.github.io/schema/vega/v5.json',
		description: 'A radar chart example, showing multiple dimensions in a radial layout.',
		random_id: Date.now(), // used to force re-rendering of the chart
		autosize: { type: 'fit', contains: 'padding' },
		padding: { left: 5, right: 5, top: 5, bottom: 5 },
		width: width,
		height: height,

		signals: [
			{ name: 'radius', update: 'width / 2.3' },
			{
				name: 'hover',
				value: {},
				on: [
					{
						events: '@category-line:mouseover',
						update: 'datum.layer_value'
					},
					{
						events: '@category-line:mouseout',
						update: '{}'
					},
					{
						events: '@value-text:mouseover',
						update: 'datum.datum.layer_value'
					},
					{
						events: '@value-text:mouseout',
						update: '{}'
					}
				]
			}
		],

		data: [
			{ name: 'table' },
			{
				name: 'points',
				source: 'table',
				transform: [
					{
						type: 'aggregate',
						groupby: ['axis_value']
					}
				]
			}
		],

		scales: [
			{
				name: 'angular',
				type: 'point',
				range: { signal: '[-PI, PI]' },
				padding: 0.5,
				domain: { data: 'table', field: 'axis_value' }
			},
			{
				name: 'radial',
				type: 'linear',
				range: { signal: '[0, radius]' },
				zero: true,
				nice: false,
				domain: { data: 'table', field: 'fixed_value' }
			},
			{
				name: 'color',
				type: 'ordinal',
				domain: { data: 'table', field: 'layer_value' },
				range: { scheme: 'category20' }
			}
		],
		legends: [
			{
				fill: 'color',
				orient: 'none',
				title: parameters.layerChannel === SlicesOrModels.SLICES ? 'slice' : 'system',
				encode: {
					legend: { update: { x: { value: -width / 2 }, y: { value: -height / 2 } } }
				}
			}
		],
		encode: {
			enter: {
				x: { signal: 'radius' },
				y: { signal: 'radius' }
			}
		},

		marks: [
			{
				type: 'group',
				name: 'categories',
				zindex: 0.5,
				from: {
					facet: { data: 'table', name: 'facet', groupby: ['layer_value'] }
				},
				marks: [
					{
						type: 'line',
						name: 'category-line',
						from: { data: 'facet' },
						encode: {
							enter: {
								interpolate: { value: 'linear-closed' },
								x: {
									signal:
										"scale('radial', datum.fixed_value) * cos(scale('angular', datum.axis_value))"
								},
								y: {
									signal:
										"scale('radial', datum.fixed_value) * sin(scale('angular', datum.axis_value))"
								}
							},
							update: {
								stroke: [{ scale: 'color', field: 'layer_value' }],
								strokeWidth: [{ test: 'datum.layer_value === hover', value: 5 }, { value: 3 }],
								strokeOpacity: [{ test: 'datum.layer_value === hover', value: 0.8 }, { value: 0.4 }]
							}
						}
					},
					{
						type: 'text',
						name: 'value-text',
						from: { data: 'category-line' },
						encode: {
							enter: {
								x: { signal: 'datum.x' },
								y: { signal: 'datum.y' }
							},
							update: {
								align: { value: 'center' },
								baseline: { value: 'middle' },
								text: { signal: 'round(100*datum.datum.fixed_value)/100' },
								fill: { value: 'black' },
								fontSize: [{ test: 'datum.datum.layer_value === hover', value: 14 }, { value: 12 }],
								fontWeight: { value: 'bold' },
								fillOpacity: [
									{ test: 'datum.datum.layer_value === hover', value: 1 },
									{ value: 0.4 }
								]
							}
						}
					}
				]
			},
			{
				type: 'rule',
				name: 'radial-grid',
				from: { data: 'points' },
				zindex: 0,
				encode: {
					enter: {
						x: { value: 0 },
						y: { value: 0 },
						x2: { signal: "radius * cos(scale('angular', datum.axis_value))" },
						y2: { signal: "radius * sin(scale('angular', datum.axis_value))" },
						stroke: { value: 'gray' },
						strokeWidth: { value: 2 },
						strokeOpacity: { value: 0.2 }
					}
				}
			},
			{
				type: 'text',
				name: 'key-label',
				from: { data: 'points' },
				zindex: 1,
				encode: {
					enter: {
						x: { signal: "(radius + 10) * cos(scale('angular', datum.axis_value))" },
						y: { signal: "(radius + 15) * sin(scale('angular', datum.axis_value))" },
						text: { field: 'axis_value' },
						align: [
							{
								test: "abs(scale('angular', datum.axis_value)) > PI / 2",
								value: 'right'
							},
							{
								value: 'left'
							}
						],
						baseline: [
							{
								test: "scale('angular', datum.axis_value) > 0",
								value: 'top'
							},
							{
								test: "scale('angular', datum.axis_value) == 0",
								value: 'middle'
							},
							{
								value: 'bottom'
							}
						],
						fill: { value: 'black' },
						fontSize: { value: 12 }
					}
				}
			}
		]
	};

	return spec as VisualizationSpec;
}
