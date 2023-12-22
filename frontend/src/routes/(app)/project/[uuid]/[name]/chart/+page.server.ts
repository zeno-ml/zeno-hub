import { getClient } from '$lib/api/client';
import type { ApiError, Chart, ChartConfig } from '$lib/zenoapi/index';
import { error } from '@sveltejs/kit';

export async function load({ params, depends, cookies, url }) {
	depends('app:charts');

	const zenoClient = await getClient(cookies, url);

	let charts: Chart[];
	let chartConfig: ChartConfig;
	try {
		charts = await zenoClient.getCharts(params.uuid);
		chartConfig = await zenoClient.getChartConfig(params.uuid);
	} catch (e) {
		const err = e as ApiError;
		throw error(err.status, err.body.detail);
	}

	return {
		charts: charts,
		chartConfig
	};
}
