<script lang="ts">
	import { goto } from '$app/navigation';

	export let data;
</script>

<div>
	{#each data.projects as project}
		<button on:click={() => goto(`/project/${project.uuid}`)} class="project-container">
			{project.name}
		</button>
	{/each}
</div>

<style>
	.project-container {
		border: solid var(--P1);
		padding: 2em;
		margin: 1em;
		border-radius: 10px;
		background-color: white;
	}
</style>
