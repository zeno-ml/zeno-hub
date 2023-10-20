import { getClient } from '$lib/api/client.js';

export async function load({ depends, cookies, url }) {
	depends('app:projects');

	const zenoClient = await getClient(cookies, url);
	const publicProjectDetails = await zenoClient.getPublicProjectsDetails();

	return {
		publicProjectDetails
	};
}
