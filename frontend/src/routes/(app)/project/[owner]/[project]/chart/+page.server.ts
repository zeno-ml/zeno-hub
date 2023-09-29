import { ZenoService, type Chart } from '$lib/zenoapi/index';
import { error } from '@sveltejs/kit';

export async function load({ params, depends }) {
	depends('app:charts');

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
