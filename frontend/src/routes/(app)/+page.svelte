<script lang="ts">
	import Project from '$lib/components/project/Project.svelte';

	export let data;

	$: ownProjects = data.projects.filter((proj) => proj.ownerName === data.user.name);
	$: sharedProjects = data.projects.filter((proj) => proj.ownerName !== data.user.name);
</script>

<div class="flex flex-col m-2">
	<h1 class="text-lg">Your projects</h1>
	<div class="mb-4 flex flex-wrap items-start">
		{#each ownProjects as project}
			<Project {project} deletable />
		{/each}
	</div>
	<h1 class="text-lg">Shared projects</h1>
	<div class="mb-4 flex flex-wrap items-start">
		{#each sharedProjects as project}
			<Project {project} />
		{/each}
	</div>
</div>
