import { getClientAndUser } from '$lib/api/client';

export const load = async ({ cookies, url }) => {
	const { zenoClient, cognitoUser } = await getClientAndUser(cookies, url);

	if (cognitoUser) {
		try {
			const user = await zenoClient.login(cognitoUser.name);
			return {
				user,
				cognitoUser
			};
		} catch {
			return {
				user: null,
				cognitoUser: null
			};
		}
	}

	return {
		user: null,
		cognitoUser: null
	};
};
