import { dev } from '$app/environment';
import { env } from '$env/dynamic/public';
import { OpenAPI, ZenoService, type User } from '$lib/zenoapi';
import { fail } from '@sveltejs/kit';

export async function load({ cookies }) {
	const userCookie = cookies.get('loggedIn');
	if (!userCookie) {
		return fail(400, {
			error: 'User could not be resolved.'
		});
	}
	const user = JSON.parse(userCookie) as User;

	OpenAPI.BASE = env.PUBLIC_BACKEND_ENDPOINT + '/api';
	const organizations = await ZenoService.getOrganizations(user);

	return {
		user: user,
		organizations: organizations
	};
}

export const actions = {
	updateUser: async ({ cookies, request }) => {
		const data = await request.formData();
		const name = data.get('name') as string;

		const userCookie = cookies.get('loggedIn');
		if (!userCookie) {
			return fail(400, {
				error: 'User could not be resolved.'
			});
		}
		const user = { ...(JSON.parse(userCookie) as User), name: name };

		OpenAPI.BASE = env.PUBLIC_BACKEND_ENDPOINT + '/api';
		await ZenoService.updateUser(user);
		cookies.set('loggedIn', JSON.stringify(user), {
			path: '/',
			httpOnly: true,
			sameSite: 'strict',
			secure: !dev,
			maxAge: 60 * 60 * 24 * 30
		});
		return { success: true };
	}
};
