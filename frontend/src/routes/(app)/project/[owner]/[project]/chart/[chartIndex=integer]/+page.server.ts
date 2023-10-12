import { getClient } from '$lib/api/client';
import type { ChartResponse } from '$lib/zenoapi';
import { error } from '@sveltejs/kit';

export async function load({ params, depends, cookies, url }) {
	depends('app:chart');

	const zenoClient = await getClient(cookies, url);
	let chartResult: ChartResponse;
	try {
		chartResult = await zenoClient.getChart(
			parseInt(params.chartIndex),
			params.owner,
			params.project
		);
	} catch (e) {
		throw error(404, 'Could not load chart');
	}

	return {
		chart: chartResult.chart,
		chartData: JSON.parse(chartResult.chartData),
		chartIndex: parseInt(params.chartIndex)
	};
}
