import { redirect } from '@sveltejs/kit';

export function load({ url }) {
	throw redirect(302, `${url.pathname}/explore`);
}
