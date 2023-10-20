<script lang="ts">
	import Project from '$lib/components/project/Project.svelte';

	export let data;
</script>

<div class="flex flex-wrap mb-6 h-full content-start">
	{#each data.publicProjectDetails as projectDetails}
		<Project project={projectDetails.project} stats={projectDetails.statistics} user={data.user} />
	{/each}
</div>
