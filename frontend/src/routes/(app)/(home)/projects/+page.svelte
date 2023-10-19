<script lang="ts">
	import Project from '$lib/components/project/Project.svelte';

	export let data;
</script>

<div class="flex flex-wrap mb-6 h-full content-start">
	{#each data.publicProjects as project}
		<Project project={project.project} stats={project.statistics} user={data.user} />
	{/each}
</div>
