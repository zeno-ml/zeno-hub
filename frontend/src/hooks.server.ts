import type { Handle } from '@sveltejs/kit';

// custom redirect from joy of code `https://github.com/JoysOfCode/sveltekit-auth-cookies/blob/migration/src/hooks.ts`
function redirect(location: string, body?: string) {
	return new Response(body, {
		status: 303,
		headers: { location }
	});
}

const unProtectedRoutes: string[] = ['/login', '/signup'];

export const handle: Handle = async ({ event, resolve }) => {
	const loggedIn = event.cookies.get('loggedIn');
	if (!loggedIn && !unProtectedRoutes.includes(event.url.pathname))
		return redirect('/login', 'No authenticated user.');

	return resolve(event);
};
