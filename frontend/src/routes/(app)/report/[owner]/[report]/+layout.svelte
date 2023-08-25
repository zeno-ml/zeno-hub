<script lang="ts">
	import { report } from '$lib/stores.js';
	import { getEndpoint } from '$lib/util/util';
	import { OpenAPI as zenoAPI } from '$lib/zenoapi';

	export let data;

	$: setupReport(data);

	function setupReport(setup_data: any) {
		report.set(setup_data.report);
		zenoAPI.BASE = `${getEndpoint()}/api`;
		if (setup_data.cognitoUser) {
			zenoAPI.HEADERS = {
				Authorization: 'Bearer ' + setup_data.cognitoUser.accessToken
			};
		}
	}
</script>

<div class="w-full h-full flex">
	<slot />
</div>
