import { env } from '$env/dynamic/public';
import { OpenAPI, ZenoService, type Project } from '$lib/zenoapi';
import { redirect } from '@sveltejs/kit';

export async function load({ cookies, url }) {
	const userCookie = cookies.get('loggedIn');
	OpenAPI.BASE = env.PUBLIC_BACKEND_ENDPOINT + '/api';
	let projects: Project[] = [];
	if (userCookie) {
		const cognitoUser = JSON.parse(userCookie);
		// If the user is not authenticated, redirect to the login page
		if (!cognitoUser.id || !cognitoUser.accessToken) {
			throw redirect(303, `/login?redirectTo=${url.pathname}`);
		}
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
