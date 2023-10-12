import { checkRefreshCookie } from '$lib/util/userCookieRefresh';
import { redirect } from '@sveltejs/kit';

export const load = async ({ cookies, url }) => {
	const cognitoUser = await checkRefreshCookie(cookies, url);
	if (cognitoUser) {
		throw redirect(303, '/');
	}
};
