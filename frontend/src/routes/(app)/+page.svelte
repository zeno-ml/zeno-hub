<script lang="ts">
	import { goto } from '$app/navigation';

	export let data;
</script>

<div>
	{#each data.projects as project}
		<button
			on:click={() => goto(`/project/${project.uuid}`)}
			class="border-solid p-2 m-1 rounded-lg border-primary-dark border-2"
		>
			{project.name}
		</button>
	{/each}
</div>
