<script lang="ts">
	import Banner from '$lib/components/general/Banner.svelte';
	import Project from '$lib/components/project/Project.svelte';

	export let data;

	$: ownProjects =
		data.user === null ? [] : data.projects.filter((proj) => proj.ownerName === data.user?.name);
	$: sharedProjects =
		data.user === null ? [] : data.projects.filter((proj) => proj.ownerName !== data.user?.name);
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
<div class="flex flex-wrap mb-6 h-full content-start">
	{#each ownProjects as project}
		<Project {project} deletable user={data.user} />
	{/each}
	{#each sharedProjects as project}
		<Project {project} user={data.user} />
	{/each}
</div>
