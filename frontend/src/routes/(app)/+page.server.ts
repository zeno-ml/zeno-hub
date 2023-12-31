import type { AuthUser } from '$lib/auth/types';
import { redirect } from '@sveltejs/kit';

export async function load({ cookies }) {
	const userCookie = cookies.get('loggedIn');
	if (!userCookie) {
		redirect(303, '/home');
	} else {
		const cognitoUser = JSON.parse(userCookie) as AuthUser;
		redirect(303, '/home/' + cognitoUser.name);
	}
}
