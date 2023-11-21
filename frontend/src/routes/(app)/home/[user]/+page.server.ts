import { redirect } from '@sveltejs/kit';

export async function load({ url, depends, parent }) {
	depends('app:reports');
	depends('app:projects');

	const { cognitoUser } = await parent();
	if (!cognitoUser) {
		throw redirect(303, `/login?redirectto=${url.pathname}`);
	}

	return {
		cognitoUser: cognitoUser
	};
}
