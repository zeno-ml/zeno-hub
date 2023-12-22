<script lang="ts">
	import { project, selectionIds, tags } from '$lib/stores';
	import type { ZenoService } from '$lib/zenoapi';
	import Button from '@smui/button';
	import { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';
	import { createEventDispatcher, getContext } from 'svelte';
	import Popup from './Popup.svelte';

	const dispatch = createEventDispatcher();
	const zenoClient = getContext('zenoClient') as ZenoService;

	let tagName = '';
	let input: Textfield;
	let originalTagName = tagName;

	$: invalidName =
		($tags.find((tag) => tag.tagName === tagName) !== undefined && tagName !== originalTagName) ||
		tagName.length === 0;

	$: if (input) {
		input.getElement().focus();
	}

	function createTag() {
		if (tagName.length === 0) {
			tagName = 'Tag ' + $tags.length;
		}

		zenoClient
			.addTag($project.uuid, {
				id: 0,
				tagName,
				dataIds: $selectionIds
			})
			.then((res) => {
				tags.update((t) => [
					...t,
					{
						id: res,
						tagName,
						dataIds: $selectionIds
					}
				]);
				selectionIds.set([]);
				dispatch('close');
			});
	}

	function submit(e: KeyboardEvent) {
		if (e.key === 'Escape') {
			dispatch('close');
		}
		if (e.key === 'Enter') {
			createTag();
		}
	}
</script>

<svelte:window on:keydown={submit} />

<Popup on:close>
	<Content class="flex items-center">
		<Textfield bind:value={tagName} label="Tag Name" bind:this={input} />
		<Button class="ml-4" variant="outlined" on:click={() => dispatch('close')}>Cancel</Button>
		<Button class="ml-2" variant="outlined" disabled={invalidName} on:click={() => createTag()}
			>{'Create'}</Button
		>
	</Content>
	{#if invalidName && tagName.length > 0}
		<p style:margin-right="10px">tag already exists</p>
	{:else if $selectionIds !== undefined && $selectionIds.length > 0}
		<p style:margin-right="10px">
			{$selectionIds.length} instance{$selectionIds.length > 1 ? 's' : ''} selected
		</p>
	{/if}
</Popup>
