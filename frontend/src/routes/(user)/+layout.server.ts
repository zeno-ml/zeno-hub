import { redirect } from '@sveltejs/kit';

export const load = async ({ cookies, url }) => {
	const userCookie = cookies.get('loggedIn');
	if (userCookie) {
		throw redirect(303, url.searchParams.get('redirectTo') ?? '/');
	}
};
