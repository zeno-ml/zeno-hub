import { verify } from '$lib/auth/cognito';
import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';

export async function load({ params }) {
	return {
		username: params.username
	};
}

export const actions: Actions = {
	verify: async ({ request, params }) => {
		const data = await request.formData();
		const code = data.get('code');
		const username = params.username;
		const failProps = {
			code: code,
			error: 'Failed to log in.'
		};

		if (!code) {
			return fail(400, {
				...failProps,
				error: 'Please enter your verification code.'
			});
		}

		try {
			await verify(username, code as string);
		} catch (error) {
			const err = error as Error;
			return fail(400, {
				...failProps,
				error: err.message
			});
		}
		throw redirect(303, '/login');
	}
};
