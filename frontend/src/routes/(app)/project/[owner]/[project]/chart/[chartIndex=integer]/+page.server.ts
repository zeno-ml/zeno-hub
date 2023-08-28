import { env } from '$env/dynamic/public';
import { OpenAPI, ZenoService } from '$lib/zenoapi/index.js';
import { error } from '@sveltejs/kit';

export async function load({ params }) {
	OpenAPI.BASE = env.PUBLIC_BACKEND_ENDPOINT + '/api';
	const uuid = await ZenoService.getProjectUuid(params.owner, params.project);
	const charts = await ZenoService.getCharts(uuid);
	const chart = charts.find((chart) => chart.id === parseInt(params.chartIndex));
	if (!charts || chart === undefined) {
		throw error(404, 'Could not load charts');
	}

	const chartData = await ZenoService.getChartData(uuid, chart);
	if (!chartData) {
		throw error(404, 'Could not load chart data');
	}

	return {
		chart: chart,
		chartData: JSON.parse(chartData),
		chartIndex: parseInt(params.chartIndex)
	};
}
