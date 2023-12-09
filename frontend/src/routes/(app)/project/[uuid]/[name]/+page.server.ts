import { getClient } from '$lib/api/client.js';

export async function load({ params, cookies, url, parent }) {
	const { project } = await parent();
	const zenoClient = await getClient(cookies, url);

	const elements = await zenoClient.getProjectHomeElements(params.uuid);

	const charts = await Promise.all(
		elements
			.filter((element) => element.type === 'CHART')
			.map(
				(element) =>
					(element.data && zenoClient.getChart(parseInt(element.data), project.uuid)) ??
					Promise.resolve(null)
			)
	);

	return {
		elements: elements,
		charts: Promise.all(charts)
	};
}
