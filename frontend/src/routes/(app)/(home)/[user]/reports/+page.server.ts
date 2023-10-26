import { getClient } from '$lib/api/client';
import type { ReportsDetails } from '$lib/zenoapi';
import { redirect } from '@sveltejs/kit';

export async function load({ cookies, depends, url }) {
	depends('app:reports');

	const zenoClient = await getClient(cookies, url);

	let reportsDetails: ReportsDetails;
	try {
		reportsDetails = await zenoClient.getReportsDetails({});
	} catch {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}

	return {
		reports: reportsDetails.reports,
		statistics: reportsDetails.statistics,
		numReports: reportsDetails.numReports
	};
}
