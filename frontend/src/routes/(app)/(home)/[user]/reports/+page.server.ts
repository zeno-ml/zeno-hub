import { getClient } from '$lib/api/client';
import type { ReportDetails } from '$lib/zenoapi';
import { redirect } from '@sveltejs/kit';

export async function load({ cookies, depends, url }) {
	depends('app:reports');

	const zenoClient = await getClient(cookies, url);
	let reportDetails: ReportDetails[] = [];

	try {
		reportDetails = await zenoClient.getReportsDetails();
	} catch {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}

	return {
		reportDetails
	};
}
