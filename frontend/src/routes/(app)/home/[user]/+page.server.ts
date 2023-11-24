import { getClient } from '$lib/api/client';
import { EntrySort, type HomeEntry } from '$lib/zenoapi';
import { redirect } from '@sveltejs/kit';

export async function load({ cookies, url, depends, parent }) {
	depends('app:reports');
	depends('app:projects');

	const { cognitoUser } = await parent();
	if (!cognitoUser) {
		throw redirect(303, `/login?redirectto=${url.pathname}`);
	}

	const zenoClient = await getClient(cookies, url);

	let homeResponse: HomeEntry[];
	try {
		homeResponse = await zenoClient.getHomeDetails({
			userName: cognitoUser.name,
			sort: EntrySort.RECENT,
			limit: 20
		});
	} catch (e) {
		throw redirect(303, `/login?redirectto=${url.pathname}`);
	}

	return {
		cognitoUser: cognitoUser,
		entries: homeResponse
	};
}
