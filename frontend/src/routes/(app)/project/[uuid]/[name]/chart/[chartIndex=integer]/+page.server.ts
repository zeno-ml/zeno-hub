import { getClient } from '$lib/api/client';
import type { ApiError, Chart, ChartConfig } from '$lib/zenoapi';
import { error } from '@sveltejs/kit';

export async function load({ params, cookies, url }) {
	const zenoClient = await getClient(cookies, url);

	let chart: Chart;
	let chartConfig: ChartConfig;
	try {
		chart = await zenoClient.getChart(parseInt(params.chartIndex), params.uuid);
		chartConfig = await zenoClient.getChartConfig(params.uuid);
	} catch (e) {
		const err = e as ApiError;
		throw error(err.status, err.body.detail);
	}

	return {
		chart,
		chartConfig,
		chartIndex: parseInt(params.chartIndex)
	};
}
