import { getEndpoint } from '$lib/util/util';
import { OpenAPI, ZenoService } from '$lib/zenoapi';

export async function load({ depends }) {
	depends('app:projects');

	OpenAPI.BASE = `${getEndpoint()}/api`;

	const publicProjects = await ZenoService.getPublicProjects();

	return {
		publicProjects: publicProjects
	};
}
