import { dev } from '$app/environment';
import { backendEndpoint } from '$lib/config';
import { OpenAPI, ZenoService } from '$lib/zenoapi';
import { fail, redirect } from '@sveltejs/kit';
import { Md5 } from 'ts-md5';
import type { Actions } from './$types';

export const actions: Actions = {
	signup: async ({ cookies, request, url }) => {
		const data = await request.formData();
		const email = data.get('email');
		const username = data.get('username');
		const password = data.get('password');
		const repeatPassword = data.get('repeatPassword');
		const failProps = {
			name: username,
			email: email,
			password: password,
			repeat: repeatPassword,
			error: 'Failed to create user.'
		};

		if (!password) {
			return fail(422, { ...failProps, error: 'Please enter a password.' });
		}
		if (!repeatPassword) {
			return fail(422, {
				...failProps,
				error: 'Please enter the password twice.'
			});
		}
		if (password !== repeatPassword) {
			return fail(422, {
				...failProps,
				error: 'Please enter the same password twice.'
			});
		}
		const secret = Md5.hashStr(password as string);
		try {
			OpenAPI.BASE = backendEndpoint + '/api';
			const user = await ZenoService.registerUser({
				id: -1,
				name: username as string,
				secret: secret,
				email: email as string
			});
			cookies.set('loggedIn', JSON.stringify(user), {
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
