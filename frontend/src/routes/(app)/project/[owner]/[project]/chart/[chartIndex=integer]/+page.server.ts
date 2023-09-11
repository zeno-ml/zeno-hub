import { getEndpoint } from '$lib/util/util';
import { OpenAPI, ZenoService, type ChartResponse } from '$lib/zenoapi/index.js';
import { error } from '@sveltejs/kit';

export async function load({ params, depends }) {
	OpenAPI.BASE = getEndpoint() + '/api';
	depends('app:chart');

	let chartResult: ChartResponse;
	try {
		chartResult = await ZenoService.getChart(
			params.owner,
			params.project,
			parseInt(params.chartIndex)
		);
	} catch (e) {
		throw error(404, 'Could not load chart');
	}

	return {
		chart: chartResult.chart,
		chartData: JSON.parse(chartResult.chartData),
		chartIndex: parseInt(params.chartIndex)
	};
}
