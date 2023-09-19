import { getEndpoint } from '$lib/util/util';
import { OpenAPI } from '$lib/zenoapi';

export async function load({ params }) {
	OpenAPI.BASE = getEndpoint() + '/api';

	return {
		compare: params.page === 'compare'
	};
}
