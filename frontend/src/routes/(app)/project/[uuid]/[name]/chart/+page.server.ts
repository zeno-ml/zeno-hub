import { getClient } from '$lib/api/client';
import type { ApiError, Chart } from '$lib/zenoapi/index';
import { error } from '@sveltejs/kit';

export async function load({ params, depends, cookies, url }) {
	depends('app:charts');

	const zenoClient = await getClient(cookies, url);

	let charts: Chart[];
	try {
		charts = await zenoClient.getCharts(params.uuid);
	} catch (e) {
		const err = e as ApiError;
		throw error(err.status, err.body.detail);
	}

	const homeChartIds = await zenoClient.projectHomeChartIds(params.uuid);

	return {
		charts: charts,
		homeChartIds: homeChartIds
	};
}
