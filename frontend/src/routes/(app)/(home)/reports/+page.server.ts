import { getClient } from '$lib/api/client';

export async function load({ depends, cookies, url }) {
	depends('app:projects');
	depends('app:reports');

	const zenoClient = await getClient(cookies, url);
	const publicReports = await zenoClient.getPublicReportsDetails();

	return {
		publicReports: publicReports
	};
}
