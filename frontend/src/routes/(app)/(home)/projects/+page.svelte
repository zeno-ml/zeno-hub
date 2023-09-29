<script lang="ts">
	import Project from '$lib/components/project/Project.svelte';

	export let data;
</script>

<div class="flex flex-wrap items-start mb-6 overflow-y-scroll h-full">
	{#each data.publicProjects as project}
		<Project {project} />
	{/each}
</div>
