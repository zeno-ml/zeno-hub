import { getClient } from '$lib/api/client';

export async function load({ cookies, url, params }) {
	const zenoClient = await getClient(cookies, url);

	const homeResponse = await zenoClient.getHomeDetails({
		limit: parseInt(params.numItems),
		userName: null
	});

	return {
		entries: homeResponse
	};
}
