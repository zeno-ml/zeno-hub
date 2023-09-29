import { ZenoService } from '$lib/zenoapi';

export async function load({ depends }) {
	depends('app:projects');

	const publicProjects = await ZenoService.getPublicProjects();

	return {
		publicProjects: publicProjects
	};
}
