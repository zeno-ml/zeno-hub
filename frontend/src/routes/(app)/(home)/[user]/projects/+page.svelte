<script lang="ts">
	import Banner from '$lib/components/general/Banner.svelte';
	import Project from '$lib/components/project/Project.svelte';

	export let data;

	$: ownProjects = data.projects.filter((proj) => proj.ownerName === data.user?.name);
	$: sharedProjects = data.projects.filter((proj) => proj.ownerName !== data.user?.name);
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
	{#each ownProjects as project, i}
		<Project {project} stats={data.statistics[i]} user={data.user} deletable />
	{/each}
	{#each sharedProjects as project, i}
		<Project {project} stats={data.statistics[i]} user={data.user} />
	{/each}
</div>
