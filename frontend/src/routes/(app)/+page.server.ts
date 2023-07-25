import { env } from '$env/dynamic/public';
import { OpenAPI, ZenoService, type ProjectConfig } from '$lib/zenoapi';

export async function load({ cookies }) {
	const userCookie = cookies.get('loggedIn');
	let projects: ProjectConfig[] = [];
	if (userCookie) {
		const user = JSON.parse(userCookie);
		OpenAPI.BASE = env.PUBLIC_BACKEND_ENDPOINT + '/api';
		projects = await ZenoService.getProjects(user);
	}

	return {
		projects: projects
	};
}
