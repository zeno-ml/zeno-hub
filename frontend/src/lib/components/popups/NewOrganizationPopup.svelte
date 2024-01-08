<script lang="ts">
	import { invalidate } from '$app/navigation';
	import type { User, ZenoService } from '$lib/zenoapi';
	import Button from '@smui/button';
	import { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';
	import { createEventDispatcher, getContext } from 'svelte';
	import Popup from '../popups/Popup.svelte';

	export let user: User;

	const zenoClient = getContext('zenoClient') as ZenoService;
	const dispatch = createEventDispatcher();

	let organizationName = '';
	let input: Textfield;

	function submit(e: KeyboardEvent) {
		if (e.key === 'Escape') {
			dispatch('close');
		}
	}

	$: if (input) {
		input.getElement().focus();
	}
</script>

<svelte:window on:keydown={submit} />
<Popup on:close>
	<Content class="flex items-center">
		<Textfield bind:value={organizationName} label="Organization Name" bind:this={input} />
		<Button class="ml-4" variant="outlined" on:click={() => dispatch('close')}>Cancel</Button>
		<Button
			class="ml-2"
			variant="outlined"
			on:click={() =>
				zenoClient
					.addOrganization({
						user: user,
						organization: { name: organizationName, id: -1, members: [], admin: true }
					})
					.then(() => {
						invalidate('app:organizations');
						dispatch('close');
					})}
			disabled={organizationName.length === 0}
		>
			Create
		</Button>
	</Content>
</Popup>
