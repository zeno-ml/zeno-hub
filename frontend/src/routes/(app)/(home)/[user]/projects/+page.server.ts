import { checkRefreshCookie } from '$lib/util/userCookieRefresh.js';
import { OpenAPI, ZenoService, type Project } from '$lib/zenoapi';
import { redirect } from '@sveltejs/kit';

export async function load({ cookies, depends, url }) {
	depends('app:projects');

	const userCookie = cookies.get('loggedIn');

	let projects: Project[] = [];
	if (!userCookie) {
		throw redirect(303, '/');
	}
	let cognitoUser = JSON.parse(userCookie);
	cognitoUser = await checkRefreshCookie(cognitoUser, cookies, url);
	OpenAPI.HEADERS = {
		Authorization: 'Bearer ' + cognitoUser.accessToken
	};
	projects = await ZenoService.getProjects();

	return {
		projects: projects
	};
}
