import { env } from '$env/dynamic/public';
import { OpenAPI, ZenoService } from '$lib/zenoapi/index.js';
import { error } from '@sveltejs/kit';

export async function load({ params }) {
	OpenAPI.BASE = env.PUBLIC_BACKEND_ENDPOINT + '/api';
	const charts = await ZenoService.getCharts(params.project);
	if (!charts) {
		throw error(404, 'Could not load charts');
	}

	return {
		charts: charts
	};
}
