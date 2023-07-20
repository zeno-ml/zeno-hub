import { dev } from '$app/environment';
import { backendEndpoint } from '$lib/config.js';
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

	OpenAPI.BASE = backendEndpoint + '/api';
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

		OpenAPI.BASE = backendEndpoint + '/api';
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
