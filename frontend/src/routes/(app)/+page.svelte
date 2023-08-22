<script lang="ts">
	import Project from '$lib/components/project/Project.svelte';

	export let data;
</script>

<div class="m-2 flex flex-wrap items-start">
	{#each data.projects as project}
		<Project {project} />
	{/each}
</div>
