import { getClient } from '$lib/api/util';
import type { Report } from '$lib/zenoapi';
import { redirect } from '@sveltejs/kit';

export async function load({ cookies, depends, url }) {
	depends('app:reports');

	const zenoClient = await getClient(cookies, url);
	let reports: Report[] = [];

	try {
		reports = await zenoClient.getReports();
	} catch {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}

	return {
		reports
	};
}
