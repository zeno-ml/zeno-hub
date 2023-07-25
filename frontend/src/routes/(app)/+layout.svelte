<script lang="ts">
	import { navigating } from '$app/stores';
	import Header from '$lib/components/general/Header.svelte';

	export let data;
</script>

<main>
	<Header user={data.user} />
	{#if Boolean($navigating)}
		<div class="container centered">
			<p>Loading...</p>
		</div>
	{:else}
		<slot />
	{/if}
</main>

<style>
	main {
		display: flex;
		flex-direction: row;
		text-align: left;
		width: 100%;
		height: 100%;
	}

	.container {
		width: 100%;
		height: 100%;
	}

	.centered {
		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>
