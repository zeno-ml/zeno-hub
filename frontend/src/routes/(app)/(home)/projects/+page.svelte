<script lang="ts">
	import Project from '$lib/components/project/Project.svelte';

	export let data;
</script>

<div class="h-full overflow-y-auto grid grid-cols-home gap-4">
	{#each data.projects as project, i}
		<Project {project} stats={data.statistics[i]} user={data.user} />
	{/each}
</div>
