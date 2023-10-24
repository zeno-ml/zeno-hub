import { getClient } from '$lib/api/client';
import type { ProjectsDetails } from '$lib/zenoapi';
import { redirect } from '@sveltejs/kit';

export async function load({ cookies, depends, url }) {
	depends('app:projects');

	const zenoClient = await getClient(cookies, url);

	let projectsDetails: ProjectsDetails;
	try {
		projectsDetails = await zenoClient.getProjectsDetails({});
	} catch (e) {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}

	return {
		projects: projectsDetails.projects,
		statistics: projectsDetails.statistics,
		numProjects: projectsDetails.numProjects
	};
}
