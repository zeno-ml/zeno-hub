import { ZenoService } from '$lib/zenoapi/index.js';
import { error } from '@sveltejs/kit';

export async function load({ params }) {
	const project = await ZenoService.getProject(params.project);
	if (!project) {
		throw error(404, 'Could not load project');
	}
	const charts = await ZenoService.getCharts(project.uuid);
	if (!charts) {
		throw error(404, 'Could not load charts');
	}

	return {
		charts: charts
	};
}
