<script lang="ts">
	import { ZenoService } from '$lib/zenoapi';
	import Button from '@smui/button/src/Button.svelte';
	import Textfield from '@smui/textfield';
	import { fade } from 'svelte/transition';
	import FeatureFlagsPopup from '../popups/FeatureFlagsPopup.svelte';

	export let email: string;
	export let name: string;

	let api_key = '';
	let copied = false;
	let showFeatureFlags = false;

	function copyKey() {
		navigator.clipboard.writeText(api_key);
		copied = true;

		// Reset copied after 3 seconds
		setTimeout(() => (copied = false), 3000);
	}
</script>

{#if showFeatureFlags}
	<FeatureFlagsPopup on:close={() => (showFeatureFlags = false)} />
{/if}
<div class="flex items-center">
	<Textfield label="Username" value={name} disabled style="margin-right: 40px;" />
	<Textfield label="Email" value={email} disabled style="margin-right: 40px;" />
</div>
<div class="mt-5">
	<Button
		variant="raised"
		class="mb-2"
		on:click={() => ZenoService.createApiKey().then((key) => (api_key = key))}
	>
		Generate new API key
	</Button>
	<p class="italic mb-4">
		Note: You can only have one API key at a time. Generating a new key will overwrite your existing
		key.
	</p>
	<Button variant="raised" class="mb-2" on:click={() => (showFeatureFlags = true)}>
		Enable feature flags
	</Button>
	<p class="italic mb-4">
		Note: Feature flags are saved as browser cookies. If you clear your cookies or switch browsers,
		your settings will be lost.
	</p>
	<div class="flex">
		{#if api_key}
			<p class="mr-3">API Key:</p>
			<h5 on:click={copyKey} on:keypress={copyKey} class="hover:text-primary cursor-pointer">
				{api_key}
			</h5>
			{#if copied}
				<p out:fade={{ delay: 250, duration: 300 }} class="ml-3 text-greenish">
					Copied API key to clipboard!
				</p>
			{/if}
		{/if}
	</div>
</div>
