import { getEndpoint } from '$lib/api/util';
import { ZenoClient } from '$lib/zenoapi';

export async function load({ depends }) {
	depends('app:projects');

	const zenoClient = new ZenoClient({
		BASE: getEndpoint()
	}).zeno;
	const publicProjects = await zenoClient.getPublicProjectsDetails();

	return {
		publicProjects: publicProjects
	};
}
