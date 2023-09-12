<script lang="ts">
	import { invalidate } from '$app/navigation';
	import { project, selectionIds, tags } from '$lib/stores';
	import { ZenoService } from '$lib/zenoapi';
	import Button from '@smui/button';
	import { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';
	import { createEventDispatcher } from 'svelte';
	import Popup from './Popup.svelte';

	const dispatch = createEventDispatcher();

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

		if ($project !== undefined) {
			ZenoService.addTag($project.uuid, {
				id: 0,
				tagName,
				dataIds: []
			}).then((res) => {
				invalidate('app:state');
				tags.update((t) => [
					...t,
					{
						id: res,
						tagName,
						dataIds: []
					}
				]);
				dispatch('close');
			});
		}
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
	<Content style="display: flex; align-items: center;">
		<Textfield bind:value={tagName} label="Tag Name" bind:this={input} />
		<Button style="margin-left: 10px;" variant="outlined" on:click={() => dispatch('close')}
			>Cancel</Button
		>
		<Button
			style="margin-left: 5px;"
			variant="outlined"
			disabled={invalidName}
			on:click={() => createTag()}>{'Create'}</Button
		>
	</Content>
	{#if invalidName && tagName.length > 0}
		<p style:margin-right="10px">tag already exists</p>
	{:else if $selectionIds !== undefined && $selectionIds.length > 0}
		<p style:margin-right="10px">
			{$selectionIds.length} instances selected
		</p>
	{/if}
</Popup>
