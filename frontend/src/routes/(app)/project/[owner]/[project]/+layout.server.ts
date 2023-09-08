import { getEndpoint, type URLParams } from '$lib/util/util';
import {
	OpenAPI,
	ZenoService,
	type FilterPredicateGroup,
	type Folder,
	type Metric,
	type Slice,
	type Tag,
	type ZenoColumn
} from '$lib/zenoapi/index.js';
import { error, redirect } from '@sveltejs/kit';

export async function load({ cookies, params, url, depends }) {
	depends('app:state');

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

	const res = await Promise.all(requests);
	const slices = res[0] as Slice[];
	const columns = res[1] as ZenoColumn[];
	const models = res[2] as string[];
	const metrics = res[3] as Metric[];
	const folders = res[4] as Folder[];
	const tags = res[5] as Tag[];

	// Get state from URL parameters.
	let urlParams: URLParams | undefined;
	let pars = '';
	if (url.searchParams.has('params')) {
		pars = url.searchParams.get('params') ?? '';
		const decodedString = atob(pars);
		if (decodedString) {
			urlParams = JSON.parse(decodedString) as URLParams;
		}
	}

	let model: string | undefined = models.length > 0 ? models[0] : undefined;
	let metric: Metric | undefined = metrics.length > 0 ? metrics[0] : undefined;
	let comparisonModel: string | undefined = models.length > 1 ? models[1] : undefined;
	let comparisonColumn: ZenoColumn | undefined = columns.find((c) => c.model === model);
	let compareSort: [ZenoColumn | undefined, boolean] = [undefined, false];
	let metricRange: [number, number] = [Infinity, -Infinity];
	let selections: {
		metadata: Record<string, FilterPredicateGroup>;
		slices: number[];
		tags: number[];
	} = {
		metadata: {},
		slices: [],
		tags: []
	};

	if (urlParams !== undefined) {
		if (urlParams.metric !== undefined) {
			urlParams.metric;
			const foundMetric = metrics.find((m) => m.id === urlParams?.metric?.id);
			if (foundMetric) {
				metric = foundMetric;
			}
		}

		if (urlParams.model) {
			if (models.find((m) => m === urlParams?.model)) {
				model = urlParams.model;
			}
		}

		if (urlParams.comparisonModel) {
			if (models.find((m) => m === urlParams?.comparisonModel)) {
				comparisonModel = urlParams.comparisonModel;
			}
		}

		if (urlParams.comparisonColumn) {
			const foundColumn = columns.find((c) => c.id === urlParams?.comparisonColumn?.id);
			if (foundColumn) {
				comparisonColumn = foundColumn;
			}
		}

		if (urlParams.compareSort) {
			compareSort = urlParams.compareSort;
		}
		if (urlParams.metricRange) {
			metricRange = urlParams.metricRange;
		}
		if (urlParams.selections) {
			selections = urlParams.selections;
		}
	}

	return {
		project: project,
		slices: slices,
		columns: columns,
		models: models,
		metrics: metrics,
		folders: folders,
		tags: tags,
		model: model,
		metric: metric,
		comparisonModel: comparisonModel,
		comparisonColumn: comparisonColumn,
		compareSort: compareSort,
		metricRange: metricRange,
		selections: selections,
		cognitoUser: cognitoUser
	};
}
