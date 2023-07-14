<script lang="ts">
	import {
		columns,
		currentProject,
		folders,
		metrics,
		models,
		projectConfig,
		rowsPerPage,
		slices,
		tags
	} from '$lib/stores';
	import { OpenAPI as zenoAPI } from '$lib/zenoapi';

	export let data;

	$: {
		currentProject.set(data.project);
		projectConfig.set(data.projectConfig);
		rowsPerPage.set(data.projectConfig.numItems ?? 5);
		slices.set(data.slices);
		columns.set(data.columns);
		models.set(data.models);
		metrics.set(data.metrics);
		folders.set(data.folders);
		tags.set(data.tags);
		zenoAPI.BASE = `/${data.project.url}/api`;
	}
</script>

<div class="container">
	<slot />
</div>

<style>
	.container {
		width: 100%;
		height: 100%;
		display: flex;
	}

	* :global(.demo-list) {
		max-width: 50px;
	}
</style>
