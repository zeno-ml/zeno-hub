<script lang="ts">
	import { ZenoService } from '$lib/zenoapi';
	import Button from '@smui/button/src/Button.svelte';
	import Textfield from '@smui/textfield';

	export let email: string;
	export let name: string;

	let api_key = '';

	function generateAPIKey() {
		ZenoService.getApiKey().then((key) => {
			api_key = key;
		});
	}
</script>

<div class="flex items-center">
	<Textfield label="Username" value={name} disabled style="margin-right: 40px;" />
	<Textfield label="Email" value={email} disabled style="margin-right: 40px;" />
</div>
<div class="mt-5">
	<div class="flex">
		<h5>API Key: {api_key}</h5>
	</div>
	<Button variant="raised" class="mt-4" on:click={generateAPIKey}>Generate new API key</Button>
	<p class="italic">
		Note: You can only have one API key at a time. Generating a new key will overwrite your existing
		key.
	</p>
</div>
