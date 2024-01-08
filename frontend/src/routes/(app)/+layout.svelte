<script lang="ts">
	import { getEndpoint } from '$lib/api/util.js';
	import { ZenoClient } from '$lib/zenoapi';
	import * as amplitude from '@amplitude/analytics-browser';
	import { setContext } from 'svelte';

	export let data;

	$: if (data.cognitoUser !== null) {
		amplitude.setUserId(data.cognitoUser.id);
		setContext(
			'zenoClient',
			new ZenoClient({
				BASE: getEndpoint(),
				TOKEN: data.cognitoUser.accessToken
			}).zeno
		);
	} else {
		setContext(
			'zenoClient',
			new ZenoClient({
				BASE: getEndpoint()
			}).zeno
		);
	}
</script>

<main class="h-full w-full text-left md:flex">
	<slot />
</main>
