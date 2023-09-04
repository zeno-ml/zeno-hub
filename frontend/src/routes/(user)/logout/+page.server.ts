import { redirect, type Actions } from '@sveltejs/kit';

export const actions: Actions = {
	default: async ({ cookies }) => {
		cookies.delete('loggedIn', { path: '/' });
		throw redirect(303, '/');
	}
};
