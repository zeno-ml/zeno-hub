import { signUpUserWithEmail } from '$lib/auth/cognito';
import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';

export const actions: Actions = {
	signup: async ({ request }) => {
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

		if ((username as string).startsWith('-')) {
			return fail(422, { ...failProps, error: 'Your username cannot start with a dash.' });
		}
		if ((username as string).search(/^[a-zA-Z0-9-]+$/)) {
			return fail(422, {
				...failProps,
				error: 'Your username may only contain alphanumeric characters or dashes.'
			});
		}
		if ((username as string).length < 3) {
			return fail(422, {
				...failProps,
				error: 'Your username must be at least 3 characters long.'
			});
		}
		if ((username as string).length > 40) {
			return fail(422, {
				...failProps,
				error: 'Your username cannot be longer than 40 characters.'
			});
		}
		if (!password) {
			return fail(422, { ...failProps, error: 'Please enter a password.' });
		}
		if (!repeatPassword) {
			return fail(422, {
				...failProps,
				error: 'Please confirm your password.'
			});
		}
		if (password !== repeatPassword) {
			return fail(422, {
				...failProps,
				error: 'Please ensure the passwords match.'
			});
		}

		try {
			await signUpUserWithEmail(username as string, email as string, password as string);
		} catch (error) {
			return fail(400, {
				...failProps,
				error: (error as Error).message
			});
		}
		redirect(303, `/verify/${username}`);
	}
};
