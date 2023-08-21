import { env } from '$env/dynamic/public';
import { OpenAPI, ZenoService } from '$lib/zenoapi/index.js';
import { error, redirect } from '@sveltejs/kit';

export async function load({ cookies, params, url }) {
	const userCookie = cookies.get('loggedIn');
	if (!userCookie) {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}
	const cognitoUser = JSON.parse(userCookie);
	// If the user is not authenticated, redirect to the login page
	if (!cognitoUser.id || !cognitoUser.accessToken) {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}

	OpenAPI.BASE = env.PUBLIC_BACKEND_ENDPOINT + '/api';
	OpenAPI.HEADERS = {
		Authorization: 'Bearer ' + cognitoUser.accessToken
	};

	const project = await ZenoService.getProject(params.project);
	if (!project) {
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
		slices: slices,
		columns: columns,
		models: models,
		metrics: metrics,
		folders: folders,
		tags: tags,
		cognitoUser: cognitoUser
	};
}
