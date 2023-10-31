import { getClient } from '$lib/api/client';
import type { HomeEntry } from '$lib/zenoapi';
import { redirect } from '@sveltejs/kit';

export async function load({ cookies, url, depends }) {
	depends('app:reports');
	depends('app:projects');

	const zenoClient = await getClient(cookies, url);

	let homeResponse: HomeEntry[];
	try {
		homeResponse = await zenoClient.getHomeDetails({});
	} catch (e) {
		throw redirect(303, `/login?redirectto=${url.pathname}`);
	}

	return {
		entries: homeResponse
	};
}
