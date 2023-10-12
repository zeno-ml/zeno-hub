import { getClient } from '$lib/api/util';
import type { Chart } from '$lib/zenoapi/index';
import { error } from '@sveltejs/kit';

export async function load({ params, depends, cookies, url }) {
	depends('app:charts');

	const zenoClient = await getClient(cookies, url);

	let charts: Chart[];
	try {
		charts = await zenoClient.getCharts(params.owner, params.project);
	} catch (e) {
		throw error(404, 'Could not load charts');
	}

	return {
		charts: charts
	};
}
