import type { AuthUser } from '$lib/auth/types.js';
import { checkRefreshCookie } from '$lib/util/userCookieRefresh.js';
import { redirect } from '@sveltejs/kit';

export const load = async ({ cookies, url }) => {
	const userCookie = cookies.get('loggedIn');

	if (userCookie) {
		let cognitoUser = JSON.parse(userCookie) as AuthUser;
		cognitoUser = await checkRefreshCookie(cognitoUser, cookies, url);
		// If the user is not authenticated, redirect to the login page
		if (!cognitoUser || !cognitoUser.id || !cognitoUser.accessToken) {
			throw redirect(303, `/login?redirectTo=${url.pathname}`);
		}

		return {
			cognitoUser
		};
	}
	return {
		cognitoUser: null
	};
};
