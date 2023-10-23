<script lang="ts">
	import Banner from '$lib/components/general/Banner.svelte';
	import Project from '$lib/components/project/Project.svelte';

	export let data;

	$: ownProjects = data.projectDetails.filter((proj) => proj.project.ownerName === data.user?.name);
	$: sharedProjects = data.projectDetails.filter(
		(proj) => proj.project.ownerName !== data.user?.name
	);
</script>

{#if ownProjects.length === 0}
	<Banner>
		Welcome to <a class="text-primary" href="https://zenoml.com">Zeno</a>! You haven't created any
		projects yet. Check out the
		<a class="text-primary" href="https://zenoml.com/docs/intro/#creating-a-project"
			>Getting Started Guide</a
		>!
	</Banner>
	<br />
{/if}
<div class="flex flex-wrap pb-6 h-full content-start overflow-y-auto">
	{#each ownProjects as project}
		<Project project={project.project} stats={project.statistics} user={data.user} deletable />
	{/each}
	{#each sharedProjects as project}
		<Project project={project.project} stats={project.statistics} user={data.user} />
	{/each}
</div>
