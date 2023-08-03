import { dev } from '$app/environment';
import { getSession, type CognitoUserSessionType } from '$lib/auth/cognito';
import type { AuthUser } from '$lib/auth/types';
import { OpenAPI } from '$lib/zenoapi';
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
				secure: !dev,
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
		throw redirect(303, url.searchParams.get('redirectTo') ?? '/');
	}
};

const extractUserFromSession = (session: CognitoUserSessionType): AuthUser => {
	if (!session?.isValid?.()) throw new Error('Invalid session');
	const user = session.getIdToken().payload;
	return {
		id: user.sub,
		name: user['cognito:username'],
		email: user.email,
		image: user.picture,
		accessToken: session.getAccessToken().getJwtToken(),
		accessTokenExpires: session.getAccessToken().getExpiration(),
		refreshToken: session.getRefreshToken().getToken()
	};
};
