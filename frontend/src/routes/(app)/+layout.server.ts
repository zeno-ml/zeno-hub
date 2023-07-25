import { backendEndpoint } from '$lib/config';
import { OpenAPI, ZenoService } from '$lib/zenoapi';
import { redirect } from '@sveltejs/kit';

export const load = async ({ cookies, url }) => {
	const userCookie = cookies.get('loggedIn');
	if (!userCookie) {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}
	const cognitoUser = JSON.parse(userCookie);
	// If the user is not authenticated, redirect to the login page
	if (!cognitoUser.id || !cognitoUser.accessToken) {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}

	OpenAPI.BASE = backendEndpoint + '/api';
	const user = await ZenoService.login(cognitoUser.email);

	return {
		user
	};
};
