import { resetPassword } from '$lib/auth/cognito';
import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';

export const actions: Actions = {
	reset: async ({ request, params }) => {
		const data = await request.formData();
		const validation = data.get('validation') as string;
		const password = data.get('password') as string;
		const repeatPassword = data.get('repeatPassword') as string;
		const username = params.username;
		const failProps = {
			validation: validation,
			password: password,
			repeat: repeatPassword,
			error: 'Failed to reset password.'
		};

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
				error: 'Please ensure your passwords match.'
			});
		}

		try {
			await resetPassword(username, validation, password);
		} catch (error) {
			return fail(400, {
				...failProps,
				error: (error as Error).message
			});
		}
		redirect(303, '/login');
	}
};
