import { getClient } from '$lib/api/client.js';

export async function load({ depends, cookies, url }) {
	depends('app:projects');

	const zenoClient = await getClient(cookies, url);
	const publicProjects = await zenoClient.getPublicProjectsDetails();

	return {
		publicProjects: publicProjects
	};
}
