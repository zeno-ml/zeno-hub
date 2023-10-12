export function POST({ cookies }) {
	cookies.delete('loggedIn', { path: '/' });
	return new Response();
}
