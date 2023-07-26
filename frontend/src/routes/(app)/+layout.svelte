<script lang="ts">
	import { navigating } from '$app/stores';
	import Header from '$lib/components/general/Header.svelte';

	export let data;
</script>

<main class="flex text-left w-full h-full">
	<Header user={data.user} />
	{#if Boolean($navigating)}
		<div class="w-full h-full flex items-center justify-center">
			<p>Loading...</p>
		</div>
	{:else}
		<slot />
	{/if}
</main>
