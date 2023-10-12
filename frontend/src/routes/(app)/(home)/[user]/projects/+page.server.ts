import { getClient } from '$lib/api/client';
import type { Project } from '$lib/zenoapi';
import { redirect } from '@sveltejs/kit';

export async function load({ cookies, depends, url }) {
	depends('app:projects');

	const zenoClient = await getClient(cookies, url);

	let projects: Project[] = [];
	try {
		projects = await zenoClient.getProjects();
	} catch (e) {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}

	return {
		projects: projects
	};
}
