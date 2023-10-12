import { getClientAndUser } from '$lib/api/util';
import { redirect } from '@sveltejs/kit';

export async function load({ cookies, url }) {
	const { zenoClient, cognitoUser } = await getClientAndUser(cookies, url);

	let user, organizations;
	try {
		user = await zenoClient.login(cognitoUser.name);
		organizations = await zenoClient.getOrganizations();
	} catch (e) {
		throw redirect(303, '/');
	}

	return {
		cognitoUser: cognitoUser,
		user: user,
		organizations: organizations
	};
}
