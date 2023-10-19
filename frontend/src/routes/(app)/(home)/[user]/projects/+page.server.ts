import { getClient } from '$lib/api/client';
import type { ProjectDetails } from '$lib/zenoapi';
import { redirect } from '@sveltejs/kit';

export async function load({ cookies, depends, url }) {
	depends('app:projects');

	const zenoClient = await getClient(cookies, url);

	let projects: ProjectDetails[] = [];
	try {
		projects = await zenoClient.getProjectsDetails();
	} catch (e) {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}

	return {
		projects: projects
	};
}
