import { env } from '$env/dynamic/public';
import { OpenAPI, ZenoService } from '$lib/zenoapi/index.js';
import { error, redirect } from '@sveltejs/kit';

export const ssr = false;

export async function load({ cookies, params, url, depends }) {
	depends('app:report');

	OpenAPI.BASE = env.PUBLIC_BACKEND_ENDPOINT + '/api';

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
	}

	const reportResponse = await ZenoService.getReport(params.owner, params.report);
	if (!reportResponse) {
		throw error(404, 'Could not load report');
	}

	return {
		report: reportResponse.report,
		reportElements: reportResponse.reportElements,
		cognitoUser: cognitoUser
	};
}
