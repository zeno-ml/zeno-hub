import { getClientAndUser } from '$lib/api/client';
import { redirect } from '@sveltejs/kit';

export async function load({ cookies, url, depends }) {
	const { zenoClient, cognitoUser } = await getClientAndUser(cookies, url);

	depends('app:organizations');

	if (!cognitoUser) {
		throw redirect(303, '/');
	}

	let user, organizations;
	try {
		user = await zenoClient.login(cognitoUser.name);
		organizations = await zenoClient.getUserOrganizations();
	} catch (e) {
		throw redirect(303, '/');
	}

	return {
		cognitoUser: cognitoUser,
		user: user,
		organizations: organizations
	};
}
