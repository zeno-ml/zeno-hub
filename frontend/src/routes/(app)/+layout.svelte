<script lang="ts">
	import { navigating } from '$app/stores';
	import Header from '$lib/components/general/Header.svelte';
	import { authToken } from '$lib/stores.js';

	export let data;
	authToken.set(data.cognitoUser.accessToken);
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
