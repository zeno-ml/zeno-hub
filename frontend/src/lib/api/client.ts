import { checkRefreshCookie } from '$lib/util/userCookieRefresh';
import { ZenoClient, type OpenAPIConfig } from '$lib/zenoapi';
import { redirect, type Cookies } from '@sveltejs/kit';
import { getEndpoint } from './util';

export async function getClient(cookies: Cookies, url: URL) {
	const res = await getClientAndUser(cookies, url);
	return res.zenoClient;
}

export async function getClientAndUser(cookies: Cookies, url: URL) {
	const serviceConfig: Partial<OpenAPIConfig> = {
		BASE: getEndpoint()
	};
	const cognitoUser = await checkRefreshCookie(cookies, url);
	if (cognitoUser && cognitoUser.id && cognitoUser.accessToken) {
		serviceConfig.TOKEN = cognitoUser.accessToken;
	} else {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}

	return { zenoClient: new ZenoClient(serviceConfig).zeno, cognitoUser };
}
