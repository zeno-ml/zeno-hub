export const backendEndpoint = 'http://127.0.0.1:8000';

export function getEndpoint() {
	if (backendEndpoint === 'http://127.0.0.1:8000') return '/localzeno';
	return backendEndpoint;
}
