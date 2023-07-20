import { redirect } from '@sveltejs/kit';

export function load({ cookies, url }) {
	const userCookie = cookies.get('loggedIn');
	if (!userCookie) {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}
	const user = JSON.parse(userCookie);

	return {
		user: user
	};
}
