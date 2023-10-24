import { getClient } from '$lib/api/client';
import type { HomepageData } from '$lib/zenoapi/models/HomepageData.js';
import { redirect } from '@sveltejs/kit';

export async function load({ cookies, depends, url, parent }) {
	depends('app:reports');

	const { user, cognitoUser } = await parent();
	if (!user || !cognitoUser) {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}

	const zenoClient = await getClient(cookies, url);

	let homepageData: HomepageData;
	try {
		homepageData = await zenoClient.getHomepageData(user.name);
	} catch {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}

	return {
		projects: homepageData.projects,
		reports: homepageData.reports,
		projectsStats: homepageData.projectsStats,
		reportsStats: homepageData.reportsStats,
		numProjects: homepageData.numProjects,
		numReports: homepageData.numReports
	};
}
