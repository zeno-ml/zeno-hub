import { dev } from '$app/environment';
import { env as public_env } from '$env/dynamic/public';
import { env as private_env } from '$env/dynamic/private';
import { extractUserFromSession, refreshAccessToken } from '$lib/auth/cognito.js';
import type { AuthUser } from '$lib/auth/types.js';
import { OpenAPI, ZenoService } from '$lib/zenoapi';
import { redirect } from '@sveltejs/kit';

export const load = async ({ cookies, url }) => {
	const userCookie = cookies.get('loggedIn');
	if (!userCookie) {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}
	const cognitoUser = JSON.parse(userCookie) as AuthUser;
	if (new Date() > new Date(cognitoUser.accessTokenExpires * 1000)) {
		try {
			const res = await refreshAccessToken(cognitoUser.refreshToken);
			const user = extractUserFromSession(res);
			OpenAPI.HEADERS = {
				Authorization: 'Bearer ' + user.accessToken
			};
			cookies.set('loggedIn', JSON.stringify(user), {
				path: '/',
				httpOnly: true,
				sameSite: 'strict',
				secure: !dev && private_env.ALLOW_INSECURE_HTTP != 'true',
				maxAge: 60 * 60 * 24 * 30
			});
		} catch (error) {
			cookies.delete('loggedIn', { path: '/' });
			throw redirect(303, `/login?redirectTo=${url.pathname}`);
		}
	}
	// If the user is not authenticated, redirect to the login page
	if (!cognitoUser.id || !cognitoUser.accessToken) {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}

	OpenAPI.BASE = public_env.PUBLIC_BACKEND_ENDPOINT + '/api';
	OpenAPI.HEADERS = {
		Authorization: 'Bearer ' + cognitoUser.accessToken
	};
	const user = await ZenoService.login(cognitoUser.name);

	return {
		user,
		cognitoUser
	};
};
