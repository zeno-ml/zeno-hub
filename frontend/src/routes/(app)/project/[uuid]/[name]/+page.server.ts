import { getClient } from '$lib/api/client.js';

export async function load({ params, cookies, url }) {
	const zenoClient = await getClient(cookies, url);

	const elements = await zenoClient.getProjectHomeElements(params.uuid);

	return {
		elements: elements
	};
}
