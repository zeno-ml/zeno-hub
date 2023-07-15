import { ZenoService } from '$lib/zenoapi/index.js';
import { error } from '@sveltejs/kit';

export async function load({ params }) {
	const project = await ZenoService.getProject(params.project);
	if (!project) {
		throw error(404, 'Could not load project');
	}
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
