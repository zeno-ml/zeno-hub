import { getEndpoint } from '$lib/util/util';
import { OpenAPI, ZenoService } from '$lib/zenoapi/index.js';
import { error } from '@sveltejs/kit';

export async function load({ params, depends }) {
	depends('app:chart');
	OpenAPI.BASE = getEndpoint() + '/api';
	const uuid = await ZenoService.getProjectUuid(params.owner, params.project);
	const charts = await ZenoService.getCharts(uuid);
	if (!charts) {
		throw error(404, 'Could not load charts');
	}

	return {
		charts: charts
	};
}
