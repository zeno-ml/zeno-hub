<script lang="ts">
	import {
		columns,
		folders,
		metrics,
		models,
		project,
		rowsPerPage,
		slices,
		tags
	} from '$lib/stores';
	import { getEndpoint } from '$lib/util/util';
	import { OpenAPI as zenoAPI } from '$lib/zenoapi';

	export let data;

	$: setupProject(data);

	// TODO: setup model, metric settings here. For some reason it's not working.
	function setupProject(setup_data: any) {
		project.set(setup_data.project);
		rowsPerPage.set(setup_data.project.samplesPerPage ?? 5);
		slices.set(setup_data.slices);
		columns.set(setup_data.columns);
		models.set(setup_data.models);
		metrics.set(setup_data.metrics);
		folders.set(setup_data.folders);
		tags.set(setup_data.tags);
		zenoAPI.BASE = `${getEndpoint()}/api`;
		if (setup_data.cognitoUser) {
			zenoAPI.HEADERS = {
				Authorization: 'Bearer ' + setup_data.cognitoUser.accessToken
			};
		}
	}
</script>

<div class="w-full h-full flex">
	<slot />
</div>
