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

	project.set(data.project);
	rowsPerPage.set(data.project.samplesPerPage ?? 10);
	slices.set(data.slices);
	columns.set(data.columns);
	models.set(data.models);
	metrics.set(data.metrics);
	folders.set(data.folders);
	tags.set(data.tags);

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
