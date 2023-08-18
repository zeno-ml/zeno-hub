<script lang="ts">
	import Project from '$lib/components/general/Project.svelte';

	export let data;
</script>

<div class="m-2">
	{#each data.projects as project}
		<Project {project} />
	{/each}
</div>
