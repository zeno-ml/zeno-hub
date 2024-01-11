import { getClient } from '$lib/api/client';
import type { ApiError, Chart, ChartConfig } from '$lib/zenoapi/index';
import { error, type NumericRange } from '@sveltejs/kit';

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
		error(err.status as NumericRange<400, 599>, err.body.detail);
	}

	const homeChartIds = await zenoClient.projectHomeChartIds(params.uuid);

	return {
		charts: charts,
		homeChartIds: homeChartIds,
		chartConfig
	};
}
