import { getClient } from '$lib/api/client.js';
import type { ApiError, ProjectHomeElement } from '$lib/zenoapi/index.js';
import { error } from '@sveltejs/kit';

export async function load({ params, cookies, url }) {
	const zenoClient = await getClient(cookies, url);

	let elements: ProjectHomeElement[];

	try {
		elements = await zenoClient.getProjectHomeElements(params.uuid);
	} catch (e) {
		const err = e as ApiError;
		throw error(err.status, err.body.detail);
	}

	return {
		elements: elements
	};
}
