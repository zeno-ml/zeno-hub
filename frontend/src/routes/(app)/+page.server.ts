import { backendEndpoint } from '$lib/config';
import { OpenAPI, ZenoService, type ProjectConfig } from '$lib/zenoapi';

export async function load({ cookies }) {
	const userCookie = cookies.get('loggedIn');
	let projects: ProjectConfig[] = [];
	if (userCookie) {
		const user = JSON.parse(userCookie);
		OpenAPI.BASE = backendEndpoint + '/api';
		projects = await ZenoService.getProjects(user);
	}

	return {
		projects: projects
	};
}
