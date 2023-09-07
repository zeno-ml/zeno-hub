<script lang="ts">
	import {
		columns,
		compareSort,
		comparisonModel,
		folders,
		metricRange,
		metrics,
		models,
		project,
		rowsPerPage,
		selections,
		slices,
		tags
	} from '$lib/stores';
	import { decodeURLParameters, getEndpoint, setURLParameters } from '$lib/util/util';
	import { OpenAPI as zenoAPI } from '$lib/zenoapi';

	export let data;

	project.set(data.project);
	rowsPerPage.set(data.project.samplesPerPage ?? 10);
	slices.set(data.slices);
	columns.set(data.columns);
	models.set(data.models);
	metrics.set(data.metrics);
	folders.set(data.folders);
	tags.set(data.tags);

	decodeURLParameters();

	// Don't update on model, metric, or comparison column change since
	// these are triggered by other subscriptions.
	comparisonModel.subscribe(() => setURLParameters());
	compareSort.subscribe(() => setURLParameters());
	metricRange.subscribe(() => setURLParameters());
	selections.subscribe(() => setURLParameters());

	zenoAPI.BASE = `${getEndpoint()}/api`;

	if (data.cognitoUser) {
		zenoAPI.HEADERS = {
			Authorization: 'Bearer ' + data.cognitoUser.accessToken
		};
	}
</script>

<div class="w-full h-full flex">
	<slot />
</div>
