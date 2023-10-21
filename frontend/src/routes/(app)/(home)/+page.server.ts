import { getClient } from '$lib/api/client';

export async function load({ cookies, url, depends }) {
	depends('app:projects');
	depends('app:reports');

	const zenoClient = await getClient(cookies, url);
	const homepageData = await zenoClient.getPublicHomepageData();

	return {
		projects: homepageData.projects,
		reports: homepageData.reports,
		numProjects: homepageData.numProjects,
		numReports: homepageData.numReports
	};
}
