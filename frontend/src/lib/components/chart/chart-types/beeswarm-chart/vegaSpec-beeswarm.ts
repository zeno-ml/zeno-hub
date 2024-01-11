import { SlicesOrModels, type BeeswarmParameters } from '$lib/zenoapi';
import type { Legend } from 'vega';
import type { VisualizationSpec } from 'vega-embed';

export default function generateSpec(
	parameters: BeeswarmParameters,
	xLabel: string,
	domain: [number, number],
	showLegend: boolean,
	width: number,
	preview: boolean
): VisualizationSpec {
	const axes = preview
		? [{ title: undefined, orient: 'bottom', scale: 'xscale', labels: false }]
		: [{ title: xLabel, titlePadding: 10, orient: 'bottom', scale: 'xscale' }];
	let legends: Legend[] = [];
	if (showLegend && !preview) {
		legends = [
			{
				type: 'symbol',
				title: parameters.colorChannel === SlicesOrModels.SLICES ? 'slice' : 'system',
				fill: 'color',
				offset: 50
			}
		];
	}

	return {
		$schema: 'https://vega.github.io/schema/vega/v5.json',
		description:
			'A beeswarm chart example that uses a force-directed layout to group items by category.',
		width: width,
		height: 100,
		random_id: Date.now(), // used to force re-rendering of the chart
		padding: { left: 5, right: 5, top: 0, bottom: 20 },
		signals: [
			{ name: 'cx', update: 'width / 2' },
			{ name: 'cy', update: 'height / 2' },
			{
				name: 'radius',
				value: 10
			},
			{
				name: 'collide',
				value: 1
			},
			{ name: 'gravityX', value: 0.2 },
			{ name: 'gravityY', value: 0.1 },
			{ name: 'static', value: true }
		],

		data: [
			{
				name: 'table'
			}
		],

		scales: [
			{
				name: 'xscale',
				domain: domain,
				range: 'width',
				nice: true,
				zero: false
			},
			{
				name: 'sizescale',
				domain: {
					data: 'table',
					field: 'size'
				},
				range: [30, 1000]
			},
			{
				name: 'color',
				type: 'ordinal',
				domain: { data: 'table', field: 'color_value' },
				range: { scheme: 'category20' }
			}
		],
		axes: axes,
		legends: legends,
		marks: [
			{
				name: 'nodes',
				type: 'symbol',
				from: { data: 'table' },
				encode: {
					enter: {
						fill: { scale: 'color', field: 'color_value' },
						xfocus: {
							scale: 'xscale',
							field: 'x_value',
							band: 0.5
						},
						yfocus: { signal: 'cy' }
					},
					update: {
						size: { scale: 'sizescale', field: 'size' },
						stroke: { value: 'white' },
						strokeWidth: { value: 1 },
						zindex: { value: 0 }
					},
					hover: {
						stroke: { value: 'black' },
						strokeWidth: { value: 3 },
						zindex: { value: 1 },
						tooltip: {
							signal: `{'size': datum.size, '${xLabel}': format(datum.x_value, '.4f'), '${
								parameters.yChannel === SlicesOrModels.MODELS ? 'system' : 'slice'
							}': datum.y_value, '${
								parameters.colorChannel === SlicesOrModels.MODELS ? 'system' : 'slice'
							}': datum.color_value}`
						}
					}
				},
				transform: [
					{
						type: 'force',
						iterations: 300,
						static: { signal: 'static' },
						forces: [
							{
								force: 'collide',
								iterations: { signal: 'collide' },
								radius: { signal: 'radius' }
							},
							{ force: 'x', x: 'xfocus', strength: { signal: 'gravityX' } },
							{ force: 'y', y: 'yfocus', strength: { signal: 'gravityY' } }
						]
					}
				]
			}
		]
	} as VisualizationSpec;
}
