import { getClient } from '$lib/api/client';
import type { ApiError, ChartResponse } from '$lib/zenoapi';
import { error } from '@sveltejs/kit';

export async function load({ params, cookies, url }) {
	const zenoClient = await getClient(cookies, url);

	let chartResult: ChartResponse;
	try {
		chartResult = await zenoClient.getChart(parseInt(params.chartIndex), params.uuid);
	} catch (e) {
		const err = e as ApiError;
		throw error(err.status, err.body.detail);
	}

	return {
		chart: chartResult.chart,
		chartData: JSON.parse(chartResult.chartData),
		chartIndex: parseInt(params.chartIndex)
	};
}
