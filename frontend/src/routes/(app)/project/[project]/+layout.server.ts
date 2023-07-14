import { connexEndpoint, localzeno } from '$lib/config.js';
import { ConnexService, OpenAPI as connexAPI } from '$lib/connexapi/index.js';
import { ZenoService, OpenAPI as zenoAPI } from '$lib/zenoapi/index.js';
import { error } from '@sveltejs/kit';

export async function load({ params }) {
	connexAPI.BASE = connexEndpoint;
	const project = await ConnexService.getProjectProjectPost(params.project);
	if (!project || !project.url) {
		throw error(404, 'Could not load project');
	}
	zenoAPI.BASE = project.url === 'localzeno' ? `${localzeno}/api` : `${project.url}/api`;
	const projectConfig = await ZenoService.getProject(project.uuid);
	if (!projectConfig) {
		throw error(404, 'Could not load project config');
	}
	const slices = await ZenoService.getSlices(project.uuid);
	if (!slices) {
		throw error(404, 'Could not load slices');
	}
	const columns = await ZenoService.getColumns(project.uuid);
	if (!columns) {
		throw error(404, 'Could not load columns');
	}
	const models = await ZenoService.getModels(project.uuid);
	if (!slices) {
		throw error(404, 'Could not load models');
	}
	const metrics = await ZenoService.getMetrics(project.uuid);
	if (!metrics) {
		throw error(404, 'Could not load metrics');
	}
	const folders = await ZenoService.getFolders(project.uuid);
	if (!folders) {
		throw error(404, 'Could not load folders');
	}
	const tags = await ZenoService.getTags(project.uuid);
	if (!tags) {
		throw error(404, 'Could not load tags');
	}

	return {
		project: project,
		projectConfig: projectConfig,
		slices: slices,
		columns: columns,
		models: models,
		metrics: metrics,
		folders: folders,
		tags: tags
	};
}
