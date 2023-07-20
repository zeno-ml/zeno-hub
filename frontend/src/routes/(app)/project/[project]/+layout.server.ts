import { backendEndpoint } from '$lib/config.js';
import { OpenAPI, ZenoService } from '$lib/zenoapi/index.js';
import { error } from '@sveltejs/kit';

export async function load({ cookies, params }) {
	const userCookie = cookies.get('loggedIn');
	if (!userCookie) {
		throw error(404, 'User not found in cookies');
	}

	OpenAPI.BASE = backendEndpoint + '/api';
	const projectConfig = await ZenoService.getProject(params.project, JSON.parse(userCookie));
	if (!projectConfig) {
		throw error(404, 'Could not load project config');
	}
	const slices = await ZenoService.getSlices(projectConfig.uuid);
	if (!slices) {
		throw error(404, 'Could not load slices');
	}
	const columns = await ZenoService.getColumns(projectConfig.uuid);
	if (!columns) {
		throw error(404, 'Could not load columns');
	}
	const models = await ZenoService.getModels(projectConfig.uuid);
	if (!slices) {
		throw error(404, 'Could not load models');
	}
	const metrics = await ZenoService.getMetrics(projectConfig.uuid);
	if (!metrics) {
		throw error(404, 'Could not load metrics');
	}
	const folders = await ZenoService.getFolders(projectConfig.uuid);
	if (!folders) {
		throw error(404, 'Could not load folders');
	}
	const tags = await ZenoService.getTags(projectConfig.uuid);
	if (!tags) {
		throw error(404, 'Could not load tags');
	}

	return {
		projectConfig: projectConfig,
		slices: slices,
		columns: columns,
		models: models,
		metrics: metrics,
		folders: folders,
		tags: tags
	};
}
