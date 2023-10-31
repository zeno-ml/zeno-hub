<script lang="ts">
	import Banner from '$lib/components/general/Banner.svelte';
	import HomeCardsContainer from '$lib/components/general/HomeCardsContainer.svelte';
	import Project from '$lib/components/project/Project.svelte';

	export let data;
</script>

{#if data.projects.length === 0}
	<Banner>
		Welcome to <a class="text-primary" href="https://zenoml.com">Zeno</a>! You haven't created any
		projects yet. Check out the
		<a class="text-primary" href="https://zenoml.com/docs/intro/#creating-a-project"
			>Getting Started Guide</a
		>!
	</Banner>
	<br />
{/if}
<HomeCardsContainer>
	{#each data.projects as project, i}
		<Project {project} stats={data.statistics[i]} user={data.user} deletable />
	{/each}
</HomeCardsContainer>
