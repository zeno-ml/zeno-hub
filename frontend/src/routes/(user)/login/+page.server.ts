import { dev } from '$app/environment';
import { env as private_env } from '$env/dynamic/private';
import { extractUserFromSession, getSession } from '$lib/auth/cognito';
import { OpenAPI, ZenoService } from '$lib/zenoapi';
import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';

export const actions: Actions = {
	login: async ({ request, cookies, url }) => {
		const data = await request.formData();
		const username = data.get('username') as string;
		const password = data.get('password') as string;
		const failProps = {
			username: username,
			password: password,
			error: 'Failed to log in.',
			showReset: false
		};

		if (!username) {
			return fail(400, {
				...failProps,
				error: 'Please enter your email address.'
			});
		}

		if (!password) {
			return fail(400, {
				...failProps,
				error: 'Please enter your password.'
			});
		}

		try {
			const res = await getSession(username, password);
			const user = extractUserFromSession(res);
			OpenAPI.HEADERS = {
				Authorization: 'Bearer ' + user.accessToken
			};
			cookies.set('loggedIn', JSON.stringify(user), {
				path: '/',
				httpOnly: true,
				sameSite: 'strict',
				secure: !dev && private_env.ALLOW_INSECURE_HTTP != 'true',
				maxAge: 60 * 60 * 24 * 30
			});
		} catch (error) {
			const err = error as Error;
			return fail(400, {
				...failProps,
				error: err.message,
				showReset: err.name === 'NotAuthorizedException'
			});
		}

		await ZenoService.login(username);
		throw redirect(303, url.searchParams.get('redirectTo') ?? '/');
	}
};
