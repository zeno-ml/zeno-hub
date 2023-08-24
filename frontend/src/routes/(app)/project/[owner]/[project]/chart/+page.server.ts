import { env } from '$env/dynamic/public';
import { OpenAPI, ZenoService } from '$lib/zenoapi/index.js';
import { error } from '@sveltejs/kit';

export async function load({ params }) {
	OpenAPI.BASE = env.PUBLIC_BACKEND_ENDPOINT + '/api';
	const uuid = await ZenoService.getProjectUuid(params.owner, params.project);
	const charts = await ZenoService.getCharts(uuid);
	if (!charts) {
		throw error(404, 'Could not load charts');
	}

	return {
		charts: charts
	};
}
