import { backendEndpoint } from '$lib/config';
import { OpenAPI, ZenoService } from '$lib/zenoapi';

export async function load() {
	OpenAPI.BASE = backendEndpoint + '/api';
	const projects = await ZenoService.getProjects();

	return {
		projects: projects
	};
}
