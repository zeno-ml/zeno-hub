<script lang="ts">
	import Project from '$lib/components/project/Project.svelte';

	export let data;

	$: ownProjects =
		data.user === null ? [] : data.projects.filter((proj) => proj.ownerName === data.user?.name);
	$: sharedProjects =
		data.user === null ? [] : data.projects.filter((proj) => proj.ownerName !== data.user?.name);
	$: publicProjects = data.publicProjects.filter(
		(proj) =>
			ownProjects.find((own) => own.uuid === proj.uuid) === undefined &&
			sharedProjects.find((shared) => shared.uuid === proj.uuid) === undefined
	);
</script>

<div class="flex flex-col m-2 ml-4">
	{#if data.user}
		{#if ownProjects.length > 0}
			<h1 class="text-xl mt-3 mb-4 ml-1">Your projects</h1>
			<div class="mb-4 flex flex-wrap items-start">
				{#each ownProjects as project}
					<Project {project} deletable />
				{/each}
			</div>
		{/if}
		{#if sharedProjects.length > 0}
			<h1 class="text-lg">Shared projects</h1>
			<div class="mb-4 flex flex-wrap items-start">
				{#each sharedProjects as project}
					<Project {project} />
				{/each}
			</div>
		{/if}
	{/if}
	{#if publicProjects.length > 0}
		<h1 class="text-lg">Public projects</h1>
		<div class="mb-4 flex flex-wrap items-start">
			{#each publicProjects as project}
				<Project {project} />
			{/each}
		</div>
	{/if}
</div>
