import { getOrRefreshCognitoUser } from '$lib/util/userCookieRefresh';
import { ZenoClient, type OpenAPIConfig } from '$lib/zenoapi';
import type { Cookies } from '@sveltejs/kit';
import { getEndpoint } from './util';

export async function getClient(cookies: Cookies, url: URL) {
	const res = await getClientAndUser(cookies, url);
	return res.zenoClient;
}

export async function getClientAndUser(cookies: Cookies, url: URL) {
	const serviceConfig: Partial<OpenAPIConfig> = {
		BASE: getEndpoint()
	};
	const cognitoUser = await getOrRefreshCognitoUser(cookies, url);
	if (cognitoUser && cognitoUser.id && cognitoUser.accessToken) {
		serviceConfig.TOKEN = cognitoUser.accessToken;
	}

	return { zenoClient: new ZenoClient(serviceConfig).zeno, cognitoUser };
}
