import { env } from '$env/dynamic/public';
import { OpenAPI, ZenoService, type Report } from '$lib/zenoapi';
import { redirect } from '@sveltejs/kit';

export async function load({ cookies, url }) {
	const userCookie = cookies.get('loggedIn');
	OpenAPI.BASE = env.PUBLIC_BACKEND_ENDPOINT + '/api';
	let reports: Report[] = [];
	if (userCookie) {
		const cognitoUser = JSON.parse(userCookie);
		// If the user is not authenticated, redirect to the login page
		if (!cognitoUser.id || !cognitoUser.accessToken) {
			throw redirect(303, `/login?redirectTo=${url.pathname}`);
		}
		OpenAPI.HEADERS = {
			Authorization: 'Bearer ' + cognitoUser.accessToken
		};
		reports = await ZenoService.getReports();
	}
	const publicReports = await ZenoService.getPublicReports();

	return {
		reports: reports,
		publicReports: publicReports
	};
}
