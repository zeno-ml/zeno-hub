import { getClientAndUser } from '$lib/api/client';

export const load = async ({ cookies, url }) => {
	const { zenoClient, cognitoUser } = await getClientAndUser(cookies, url);

	if (cognitoUser) {
		const user = await zenoClient.login(cognitoUser.name);
		return {
			user,
			cognitoUser
		};
	}

	return {
		user: null,
		cognitoUser: null
	};
};
