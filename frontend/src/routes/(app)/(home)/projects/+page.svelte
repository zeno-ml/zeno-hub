<script lang="ts">
	import HomeCardsContainer from '$lib/components/general/HomeCardsContainer.svelte';
	import Project from '$lib/components/project/Project.svelte';

	export let data;
</script>

<HomeCardsContainer>
	{#each data.projects as project, i}
		<Project {project} stats={data.statistics[i]} user={data.user} />
	{/each}
</HomeCardsContainer>
