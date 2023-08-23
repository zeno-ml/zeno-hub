<script lang="ts">
	import { navigating } from '$app/stores';
	import Header from '$lib/components/general/Header.svelte';
	import { authToken } from '$lib/stores.js';
	import { getEndpoint } from '$lib/util/util.js';
	import { OpenAPI } from '$lib/zenoapi/index.js';

	export let data;
	if (data.cognitoUser !== null) {
		authToken.set(data.cognitoUser.accessToken);
	}

	$: {
		OpenAPI.BASE = `${getEndpoint()}/api`;
		if (data.cognitoUser !== null) {
			OpenAPI.HEADERS = {
				Authorization: 'Bearer ' + data.cognitoUser.accessToken
			};
		}
	}
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
