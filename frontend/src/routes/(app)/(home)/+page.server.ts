import type { AuthUser } from '$lib/auth/types';
import { redirect } from '@sveltejs/kit';

export async function load({ cookies }) {
	const userCookie = cookies.get('loggedIn');

	if (!userCookie) {
		throw redirect(303, '/projects');
	} else {
		const cognitoUser = JSON.parse(userCookie) as AuthUser;
		throw redirect(303, '/' + cognitoUser.name + '/projects');
	}
}
