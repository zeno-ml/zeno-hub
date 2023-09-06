import { getEndpoint } from '$lib/util/util';
import {
	OpenAPI,
	ZenoService,
	type Folder,
	type Metric,
	type Slice,
	type Tag,
	type ZenoColumn
} from '$lib/zenoapi/index.js';
import { error, redirect } from '@sveltejs/kit';

export async function load({ cookies, params, url }) {
	OpenAPI.BASE = getEndpoint() + '/api';

	const projectPublic = ZenoService.isProjectPublic(params.project);

	let cognitoUser = null;
	const userCookie = cookies.get('loggedIn');
	if (userCookie) {
		cognitoUser = JSON.parse(userCookie);
		// If the user is not authenticated, redirect to the login page
		if (!cognitoUser.id || !cognitoUser.accessToken) {
			throw redirect(303, `/login?redirectTo=${url.pathname}`);
		}
		OpenAPI.HEADERS = {
			Authorization: 'Bearer ' + cognitoUser.accessToken
		};
	} else if (!projectPublic) {
		throw redirect(303, `/login?redirectTo=${url.pathname}`);
	}

	const project = await ZenoService.getProject(params.owner, params.project);
	if (!project) {
		throw error(404, 'Could not load project config');
	}

	const requests = [
		ZenoService.getSlices(project.uuid),
		ZenoService.getColumns(project.uuid),
		ZenoService.getModels(project.uuid),
		ZenoService.getMetrics(project.uuid),
		ZenoService.getFolders(project.uuid),
		ZenoService.getTags(project.uuid)
	];

	const results = await Promise.all(requests);

	return {
		project: project,
		slices: results[0] as Slice[],
		columns: results[1] as ZenoColumn[],
		models: results[2] as string[],
		metrics: results[3] as Metric[],
		folders: results[4] as Folder[],
		tags: results[5] as Tag[],
		cognitoUser: cognitoUser
	};
}
