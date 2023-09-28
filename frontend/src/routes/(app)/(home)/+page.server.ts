import { redirect } from '@sveltejs/kit';

export async function load({ cookies }) {
	const userCookie = cookies.get('loggedIn');

	if (!userCookie) {
		throw redirect(303, '/public');
	} else {
		throw redirect(303, '/my');
	}
}
