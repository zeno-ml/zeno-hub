import { browser } from '$app/environment';
import { env } from '$env/dynamic/public';

export function getEndpoint() {
	if (env.PUBLIC_BACKEND_ENDPOINT == 'http://zeno-backend:8000') {
		if (browser) {
			return '/dockerzeno';
		}
		return 'http://zeno-backend:8000';
	}
	return env.PUBLIC_BACKEND_ENDPOINT;
}
