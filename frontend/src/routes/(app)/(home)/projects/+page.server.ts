import { getClient } from '$lib/api/client.js';

export async function load({ depends, cookies, url }) {
	depends('app:projects');

	const zenoClient = await getClient(cookies, url);
	const publicProjectsDetails = await zenoClient.getPublicProjectsDetails({});

	return {
		projects: publicProjectsDetails.projects,
		statistics: publicProjectsDetails.statistics,
		numProjects: publicProjectsDetails.numProjects
	};
}
