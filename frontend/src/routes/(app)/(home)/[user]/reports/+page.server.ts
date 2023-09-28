import { checkRefreshCookie } from '$lib/util/userCookieRefresh.js';
import { getEndpoint } from '$lib/util/util';
import { OpenAPI, ZenoService, type Report } from '$lib/zenoapi';
import { redirect } from '@sveltejs/kit';

export async function load({ cookies, depends, url }) {
	depends('app:reports');

	OpenAPI.BASE = `${getEndpoint()}/api`;

	const userCookie = cookies.get('loggedIn');

	let reports: Report[] = [];
	if (!userCookie) {
		throw redirect(303, '/');
	}
	let cognitoUser = JSON.parse(userCookie);
	cognitoUser = await checkRefreshCookie(cognitoUser, cookies, url);
	OpenAPI.HEADERS = {
		Authorization: 'Bearer ' + cognitoUser.accessToken
	};
	reports = await ZenoService.getReports();

	return {
		reports: reports
	};
}
