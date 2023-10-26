<script lang="ts">
	import Project from '$lib/components/project/Project.svelte';

	export let data;
</script>

<div class="flex flex-wrap pb-6 h-full content-start overflow-y-auto">
	{#each data.projects as project, i}
		<Project {project} stats={data.statistics[i]} user={data.user} />
	{/each}
</div>
