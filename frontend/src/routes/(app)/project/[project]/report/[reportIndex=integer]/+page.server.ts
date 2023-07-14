import { connexEndpoint, localzeno } from '$lib/config.js';
import { ConnexService, OpenAPI as connexAPI } from '$lib/connexapi/index.js';
import { ZenoService, OpenAPI as zenoAPI } from '$lib/zenoapi/index.js';
import { error } from '@sveltejs/kit';

export async function load({ params }) {
	connexAPI.BASE = connexEndpoint;
	const project = await ConnexService.getProject(params.project);
	if (!project || !project.url) {
		throw error(404, 'Could not load project');
	}
	zenoAPI.BASE = project.url === 'localzeno' ? `${localzeno}/api` : `${project.url}/api`;
	const charts = await ZenoService.getCharts(project.uuid);
	const chart = charts.find((chart) => chart.id === parseInt(params.reportIndex));
	if (!charts || chart === undefined) {
		throw error(404, 'Could not load charts');
	}
	const chartData = await ZenoService.getChartData(project.uuid, chart);
	if (!chartData) {
		throw error(404, 'Could not load chart data');
	}

	return {
		chart: chart,
		chartData: JSON.parse(chartData),
		reportIndex: parseInt(params.reportIndex)
	};
}
