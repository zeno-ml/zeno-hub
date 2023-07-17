import { backendEndpoint } from '$lib/config.js';
import { OpenAPI, ZenoService } from '$lib/zenoapi/index.js';
import { error } from '@sveltejs/kit';

export async function load({ params }) {
	OpenAPI.BASE = backendEndpoint + '/api';
	const charts = await ZenoService.getCharts(params.project);
	const chart = charts.find((chart) => chart.id === parseInt(params.reportIndex));
	if (!charts || chart === undefined) {
		throw error(404, 'Could not load charts');
	}
	const chartData = await ZenoService.getChartData(params.project, chart);
	if (!chartData) {
		throw error(404, 'Could not load chart data');
	}

	return {
		chart: chart,
		chartData: JSON.parse(chartData),
		reportIndex: parseInt(params.reportIndex)
	};
}
