import { env } from '$env/dynamic/public';
import { OpenAPI, ZenoService } from '$lib/zenoapi/index.js';
import { error, redirect } from '@sveltejs/kit';

export async function load({ cookies, params, url }) {
	OpenAPI.BASE = env.PUBLIC_BACKEND_ENDPOINT + '/api';

	const reportPublic = ZenoService.isProjectPublic(params.report);

	let cognitoUser = null;
	const userCookie = cookies.get('loggedIn');
	if (userCookie) {
		cognitoUser = JSON.parse(userCookie);
		// If the user is not authenticated, redirect to the login page
		if (!cognitoUser.id || !cognitoUser.accessToken) {
			throw redirect(303, `/login?redirectTo=${url.pathname}`);
		}
		OpenAPI.HEADERS = {
			Authorization: 'Bearer ' + cognitoUser.accessToken
		};
	} else if (!reportPublic) {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}

	const report = await ZenoService.getReport(params.owner, params.report);
	if (!report) {
		throw error(404, 'Could not load report');
	}

	return {
		report: report,
		cognitoUser: cognitoUser
	};
}
