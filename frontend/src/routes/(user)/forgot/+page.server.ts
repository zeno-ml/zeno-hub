import { sendPasswordResetCode } from '$lib/auth/cognito';
import { redirect, type Actions } from '@sveltejs/kit';

export const actions: Actions = {
	code: async ({ request }) => {
		const data = await request.formData();
		const username = data.get('username') as string;
		sendPasswordResetCode(username);
		throw redirect(303, `/forgot/${username}`);
	}
};
