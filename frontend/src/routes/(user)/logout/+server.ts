import { OpenAPI } from '$lib/zenoapi';

export function POST({ cookies }) {
	cookies.delete('loggedIn', { path: '/' });
	OpenAPI.HEADERS = {};
	return new Response();
}
