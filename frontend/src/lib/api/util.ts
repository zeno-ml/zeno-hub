import { browser } from '$app/environment';
import { env } from '$env/dynamic/public';

export function getEndpoint() {
	if (env.PUBLIC_BACKEND_ENDPOINT == 'http://zeno-backend:8000') {
		if (browser) {
			return '/dockerzeno/api';
		}
		return 'http://zeno-backend:8000/api';
	} else if (env.PUBLIC_BACKEND_ENDPOINT == 'http://zeno-backend-test:8000') {
		if (browser) {
			return '/testdockerzeno/api';
		}
		return 'http://zeno-backend-test:8000/api';
	}
	return env.PUBLIC_BACKEND_ENDPOINT + '/api';
}
