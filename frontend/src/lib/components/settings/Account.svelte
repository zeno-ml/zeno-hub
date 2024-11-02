<script lang="ts">
	import { page } from '$app/stores';
	import type { User, ZenoService } from '$lib/zenoapi';
	import Button from '@smui/button';
	import Textfield from '@smui/textfield';
	import { getContext } from 'svelte';
	import { fade } from 'svelte/transition';
	import FeatureFlagsPopup from '../popups/FeatureFlagsPopup.svelte';

	export let email: string;
	export let user: User;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let api_key = '';
	let copied = false;
	let showFeatureFlags = false;
	let displayNameChanged = false;
	let displayName = user.displayName;

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
<div class="flex flex-wrap items-center gap-4 gap-x-10">
	<Textfield label="Username" value={user.name} disabled />
	<Textfield label="Email" value={email} disabled />
	<Textfield
		label="Display Name"
		bind:value={displayName}
		on:input={() => (displayNameChanged = true)}
	/>
	{#if displayNameChanged}
		<div class="flex gap-2" in:fade={{ duration: 300 }}>
			<Button
				variant="outlined"
				on:click={() => {
					displayNameChanged = false;
					displayName = user.displayName;
				}}
			>
				Cancel
			</Button>
			<Button
				variant="raised"
				on:click={() =>
					zenoClient.updateUser({ ...user, displayName }).then(() => (displayNameChanged = false))}
			>
				Update
			</Button>
		</div>
	{/if}
</div>
<div class="mt-5">
	{#if $page.url.origin !== 'https://hub.zenoml.com'}
		<Button variant="raised" class="mb-2" on:click={() => (showFeatureFlags = true)}>
			Configure feature flags
		</Button>
		<p class="mb-4 italic">
			Note: Feature flags are saved as browser cookies. If you clear your cookies or switch
			browsers, your settings will be lost.
		</p>
	{/if}
	<Button
		variant="raised"
		class="mb-2"
		on:click={() => zenoClient.createApiKey().then((key) => (api_key = key))}
	>
		Generate new API key
	</Button>
	<p class="mb-2 italic">
		Note: You can only have one API key at a time. Generating a new key will overwrite your existing
		key.
	</p>
	<div class="mb-4 flex">
		{#if api_key}
			<p class="mr-3">API Key:</p>
			<button on:click={copyKey} on:keypress={copyKey} class="cursor-pointer hover:text-primary">
				{api_key}
			</button>
			{#if copied}
				<p out:fade={{ delay: 250, duration: 300 }} class="ml-3 text-secondary">
					Copied API key to clipboard!
				</p>
			{/if}
		{/if}
	</div>
</div>
