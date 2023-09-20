import { env } from '$env/dynamic/public';
import { checkRefreshCookie } from '$lib/util/userCookieRefresh.js';
import { ApiError, OpenAPI, ZenoService, type ReportResponse } from '$lib/zenoapi';
import { error, redirect } from '@sveltejs/kit';

export const ssr = false;

export async function load({ cookies, params, url }) {
	OpenAPI.BASE = env.PUBLIC_BACKEND_ENDPOINT + '/api';

	let cognitoUser = null;
	const userCookie = cookies.get('loggedIn');
	if (userCookie) {
		cognitoUser = JSON.parse(userCookie);
		cognitoUser = await checkRefreshCookie(cognitoUser, cookies, url);
		// If the user is not authenticated, redirect to the login page
		if (!cognitoUser.id || !cognitoUser.accessToken) {
			throw redirect(303, `/login?redirectTo=${url.pathname}`);
		}
		OpenAPI.HEADERS = {
			Authorization: 'Bearer ' + cognitoUser.accessToken
		};
	}

	let reportResponse: ReportResponse;
	try {
		reportResponse = await ZenoService.getReport(params.owner, params.report);
	} catch (e: unknown) {
		if ((e as ApiError).status === 401) {
			if (cognitoUser !== null) {
				throw redirect(303, `/auth`);
			} else {
				throw redirect(303, `/login?redirectTo=${url.pathname}`);
			}
		}
		throw error(404, 'Could not load report');
	}

	return {
		report: reportResponse.report,
		reportElements: reportResponse.reportElements,
		cognitoUser: cognitoUser
	};
}
