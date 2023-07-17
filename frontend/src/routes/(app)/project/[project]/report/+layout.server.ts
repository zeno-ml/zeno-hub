import { backendEndpoint } from '$lib/config.js';
import { OpenAPI, ZenoService } from '$lib/zenoapi/index.js';
import { error } from '@sveltejs/kit';

export async function load({ params }) {
	OpenAPI.BASE = backendEndpoint + '/api';
	const charts = await ZenoService.getCharts(params.project);
	if (!charts) {
		throw error(404, 'Could not load charts');
	}

	return {
		charts: charts
	};
}
