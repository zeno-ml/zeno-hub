import { getClientAndUser } from '$lib/api/util';
import type { URLParams } from '$lib/util/util';
import type {
	ApiError,
	FilterPredicateGroup,
	Metric,
	ProjectState,
	ZenoColumn
} from '$lib/zenoapi/index.js';
import { error, redirect } from '@sveltejs/kit';

export const ssr = false;

export async function load({ cookies, params, url }) {
	const { zenoClient, cognitoUser } = await getClientAndUser(cookies, url);

	let project_result: ProjectState;
	try {
		project_result = await zenoClient.getProjectState(params.owner, params.project);
	} catch (e: unknown) {
		if ((e as ApiError).status === 401) {
			if (cognitoUser !== null) {
				throw redirect(303, `/auth`);
			} else {
				throw redirect(303, `/login?redirectTo=${url.pathname}`);
			}
		}
		throw error(404, 'Could not load project configuration');
	}

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

	let model: string | undefined =
		project_result.models.length > 0 ? project_result.models[0] : undefined;
	let metric: Metric | undefined =
		project_result.metrics.length > 0 ? project_result.metrics[0] : undefined;
	let comparisonModel: string | undefined =
		project_result.models.length > 1 ? project_result.models[1] : undefined;
	let comparisonColumn: ZenoColumn | undefined = project_result.columns.find(
		(c) => c.model === model
	);
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
			const foundMetric = project_result.metrics.find((m) => m.id === urlParams?.metric?.id);
			if (foundMetric) {
				metric = foundMetric;
			}
		}

		if (urlParams.model) {
			if (project_result.models.find((m) => m === urlParams?.model)) {
				model = urlParams.model;
			}
		}

		if (urlParams.comparisonModel) {
			if (project_result.models.find((m) => m === urlParams?.comparisonModel)) {
				comparisonModel = urlParams.comparisonModel;
			}
		}

		if (urlParams.comparisonColumn) {
			const foundColumn = project_result.columns.find(
				(c) => c.id === urlParams?.comparisonColumn?.id
			);
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
		project: project_result.project,
		slices: project_result.slices,
		columns: project_result.columns,
		models: project_result.models,
		metrics: project_result.metrics,
		folders: project_result.folders,
		tags: project_result.tags,
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
