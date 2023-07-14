import { fail } from '@sveltejs/kit';
import { redirect } from '@sveltejs/kit';
import { Md5 } from 'ts-md5';
import { dev } from '$app/environment';
import type { Actions } from './$types';
import { ConnexService, OpenAPI } from '$lib/connexapi';
import { connexEndpoint } from '$lib/config';
import { isConnexAPIError } from '$lib/util/util';

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
			await ConnexService.loginLoginPost({
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
				error: isConnexAPIError(error) ? error.body.detail : 'Unknown error'
			});
		}

		throw redirect(303, url.searchParams.get('redirectTo') ?? '/');
	}
};
