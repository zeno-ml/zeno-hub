import { getClient } from '$lib/api/client';
import type { AuthUser } from '$lib/auth/types';
import { HomeSort, type HomeEntry } from '$lib/zenoapi';
import { redirect } from '@sveltejs/kit';

export async function load({ cookies, url, depends }) {
	depends('app:reports');
	depends('app:projects');

	const userCookie = cookies.get('loggedIn');

	let cognitoUser: AuthUser;
	if (userCookie) {
		cognitoUser = JSON.parse(userCookie) as AuthUser;
		// If the user is not authenticated, redirect to the login page
		if (!cognitoUser || !cognitoUser.id || !cognitoUser.accessToken) {
			throw redirect(303, `/login?redirectTo=${url.pathname}`);
		}
	} else {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}

	const zenoClient = await getClient(cookies, url);

	let homeResponse: HomeEntry[];
	try {
		homeResponse = await zenoClient.getHomeDetails({
			userName: cognitoUser.name,
			sort: HomeSort.RECENT
		});
	} catch (e) {
		throw redirect(303, `/login?redirectto=${url.pathname}`);
	}

	return {
		cognitoUser: cognitoUser,
		entries: homeResponse
	};
}
