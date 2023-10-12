import { browser } from '$app/environment';
import { env } from '$env/dynamic/public';
import { ZenoClient, type OpenAPIConfig } from '$lib/zenoapi';
import { redirect, type Cookies } from '@sveltejs/kit';

export function getEndpoint() {
	if (env.PUBLIC_BACKEND_ENDPOINT == 'http://zeno-backend:8000') {
		if (browser) {
			return '/dockerzeno/api';
		}
		return 'http://zeno-backend:8000/api';
	}
	return env.PUBLIC_BACKEND_ENDPOINT + '/api';
}

export async function getClient(cookies: Cookies, url: URL) {
	const res = await getClientAndUser(cookies, url);
	return res.zenoClient;
}

export async function getClientAndUser(cookies: Cookies, url: URL) {
	let cognitoUser = null;
	const serviceConfig: Partial<OpenAPIConfig> = {
		BASE: getEndpoint()
	};
	const userCookie = cookies.get('loggedIn');
	if (userCookie) {
		cognitoUser = JSON.parse(userCookie);
		// If the user is not authenticated, redirect to the login page
		if (!cognitoUser.id || !cognitoUser.accessToken) {
			throw redirect(303, `/login?redirectTo=${url.pathname}`);
		}
		serviceConfig.TOKEN = cognitoUser.accessToken;
	}

	return { zenoClient: new ZenoClient(serviceConfig).zeno, cognitoUser };
}
