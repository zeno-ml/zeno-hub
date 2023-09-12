import { dev } from '$app/environment';
import { env as private_env } from '$env/dynamic/private';

export async function POST({ request, cookies }) {
	const data = await request.json();
	cookies.set('featureFlags', JSON.stringify(data), {
		path: '/',
		httpOnly: true,
		sameSite: 'strict',
		secure: !dev && private_env.ALLOW_INSECURE_HTTP != 'true',
		maxAge: 60 * 60 * 24 * 30
	});
	return new Response();
}
