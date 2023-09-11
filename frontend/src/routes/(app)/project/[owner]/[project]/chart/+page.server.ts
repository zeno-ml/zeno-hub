import { getEndpoint } from '$lib/util/util';
import { OpenAPI, ZenoService, type Chart } from '$lib/zenoapi/index';
import { error } from '@sveltejs/kit';

export async function load({ params, depends }) {
	depends('app:charts');

	OpenAPI.BASE = getEndpoint() + '/api';

	let charts: Chart[];
	try {
		charts = await ZenoService.getCharts(params.owner, params.project);
	} catch (e) {
		throw error(404, 'Could not load charts');
	}

	return {
		charts: charts
	};
}
