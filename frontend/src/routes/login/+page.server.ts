import { dev } from '$app/environment';
import { connexEndpoint } from '$lib/config';
import { ConnexService, OpenAPI } from '$lib/connexapi';
import { fail, redirect } from '@sveltejs/kit';
import { Md5 } from 'ts-md5';
import type { Actions } from './$types';

export const actions: Actions = {
	login: async ({ request, cookies, url }) => {
		const data = await request.formData();
		const email = data.get('email');
		const password = data.get('password');
		const failProps = {
			email: email,
			password: password,
			error: 'Failed to log in.'
		};

		if (!email) {
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

		const secret = Md5.hashStr(password as string);
		try {
			OpenAPI.BASE = connexEndpoint;
			await ConnexService.login({
				secret: secret,
				email: email as string
			});
			cookies.set('loggedIn', 'loggedIn', {
				path: '/',
				httpOnly: true,
				sameSite: 'strict',
				secure: !dev,
				maxAge: 60 * 60 * 24 * 30
			});
		} catch (error) {
			return fail(400, {
				...failProps,
				error: error
			});
		}

		throw redirect(303, url.searchParams.get('redirectTo') ?? '/');
	}
};
