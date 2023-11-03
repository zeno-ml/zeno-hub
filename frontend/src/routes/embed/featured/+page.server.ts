import { getClient } from '$lib/api/client';

export async function load({ cookies, url }) {
	const zenoClient = await getClient(cookies, url);

	const homeResponse = await zenoClient.getHomeDetails({ limit: 3, userName: null });

	return {
		entries: homeResponse
	};
}
