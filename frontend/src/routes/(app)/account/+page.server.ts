import { getEndpoint } from '$lib/util/util';
import { OpenAPI, ZenoService } from '$lib/zenoapi';
import { redirect } from '@sveltejs/kit';

export async function load({ cookies, url }) {
	const userCookie = cookies.get('loggedIn');
	if (!userCookie) {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}
	const cognitoUser = JSON.parse(userCookie);
	// If the user is not authenticated, redirect to the login page
	if (!cognitoUser.id || !cognitoUser.accessToken) {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}

	OpenAPI.BASE = getEndpoint() + '/api';
	OpenAPI.HEADERS = {
		Authorization: 'Bearer ' + cognitoUser.accessToken
	};
	const user = await ZenoService.login(cognitoUser.name);
	const organizations = await ZenoService.getOrganizations();

	return {
		cognitoUser: cognitoUser,
		user: user,
		organizations: organizations
	};
}
