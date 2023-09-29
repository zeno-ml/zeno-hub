<script lang="ts">
	import Project from '$lib/components/project/Project.svelte';

	export let data;
</script>

<div class="flex flex-wrap items-start mb-6">
	{#each data.publicProjects as project}
		<Project {project} />
	{/each}
</div>
