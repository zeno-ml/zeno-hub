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
		Welcome to <a class="text-primary" href="https://zenoml.com">Zeno</a>! You don't have any
		projects yet. Create one with the
		<a class="text-primary" href="https://github.com/zeno-ml/zeno-client">Zeno Client.</a>
	</Banner>
{/if}
<div class="flex flex-wrap mb-6 overflow-y-scroll h-full">
	{#each ownProjects as project}
		<Project {project} deletable />
	{/each}
	{#each sharedProjects as project}
		<Project {project} />
	{/each}
</div>
