<script lang="ts">
	import { featureFlags } from '$lib/stores';
	import { zenoFeatureFlags } from '$lib/util/features';
	import Button from '@smui/button/src/Button.svelte';
	import Checkbox from '@smui/checkbox/src/Checkbox.svelte';
	import { Content } from '@smui/paper';
	import { createEventDispatcher } from 'svelte';
	import Popup from './Popup.svelte';

	const dispatch = createEventDispatcher();

	function submit(e: KeyboardEvent) {
		if (e.key === 'Escape') {
			dispatch('close');
		}
		if (e.key === 'Enter') {
			dispatch('close');
		}
	}

	function updateFlag(flag: string) {
		fetch('/api/features', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ ...$featureFlags, [flag]: !$featureFlags[flag] })
		});
		featureFlags.set({ ...$featureFlags, [flag]: !$featureFlags[flag] });
	}
</script>

<svelte:window on:keydown={submit} />
<Popup on:close>
	<Content class="flex w-[400px] flex-col">
		<h2 class="mb-4 text-xl">Feature Flags</h2>
		{#each Object.keys($featureFlags).filter( (key) => Object.keys(zenoFeatureFlags).includes(key) ) as flag}
			<div class="flex items-center">
				<Checkbox checked={$featureFlags[flag]} on:change={() => updateFlag(flag)} />
				<p>{flag}</p>
			</div>
		{/each}
		<div class="flex items-center self-end">
			<Button variant="outlined" on:click={() => dispatch('close')}>{'Done'}</Button>
		</div>
	</Content>
</Popup>
