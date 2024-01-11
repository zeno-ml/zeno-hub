import { getOrRefreshCognitoUser } from '$lib/util/userCookieRefresh';
import { redirect } from '@sveltejs/kit';

export const load = async ({ cookies, url }) => {
	const cognitoUser = await getOrRefreshCognitoUser(cookies, url);
	if (cognitoUser) {
		redirect(303, '/');
	}
};
