import { getEndpoint } from '$lib/util/util';
import { OpenAPI, ZenoService, type Project } from '$lib/zenoapi';

export async function load({ cookies }) {
	OpenAPI.BASE = `${getEndpoint()}/api`;

	let projects: Project[] = [];
	const userCookie = cookies.get('loggedIn');
	if (userCookie) {
		const cognitoUser = JSON.parse(userCookie);
		OpenAPI.HEADERS = {
			Authorization: 'Bearer ' + cognitoUser.accessToken
		};
		projects = await ZenoService.getProjects();
	}

	const publicProjects = await ZenoService.getPublicProjects();

	return {
		projects: projects,
		publicProjects: publicProjects
	};
}
