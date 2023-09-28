import { ZenoService, type ChartResponse } from '$lib/zenoapi/index.js';
import { error } from '@sveltejs/kit';

export async function load({ params, depends }) {
	depends('app:chart');

	let chartResult: ChartResponse;
	try {
		chartResult = await ZenoService.getChart(
			parseInt(params.chartIndex),
			params.owner,
			params.project
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
