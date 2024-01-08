import { redirect } from '@sveltejs/kit';

export function load({ url }) {
	redirect(302, `${url.pathname}/explore`);
}
