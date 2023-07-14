import { connexEndpoint } from '$lib/config.js';
import { ConnexService, OpenAPI as connexAPI } from '$lib/connexapi/index.js';

export async function load() {
	connexAPI.BASE = connexEndpoint;
	const projects = await ConnexService.getAllProjectsAllProjectsPost();

	return {
		projects: projects
	};
}
