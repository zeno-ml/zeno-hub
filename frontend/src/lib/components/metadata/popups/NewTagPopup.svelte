<script lang="ts">
	import { projectConfig, selectionIds, showNewTag, tags } from '$lib/stores';
	import { clickOutside } from '$lib/util/clickOutside';
	import { ZenoService } from '$lib/zenoapi';
	import Button from '@smui/button';
	import Paper, { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';

	let tagName = '';
	let input: Textfield;
	let originalTagName = tagName;

	$: invalidName =
		($tags.find((tag) => tag.tagName === tagName) !== undefined && tagName !== originalTagName) ||
		tagName.length === 0;

	$: if ($showNewTag && input) {
		input.getElement().focus();
	}

	function createTag() {
		if (tagName.length === 0) {
			tagName = 'Tag ' + $tags.length;
		}

		if ($projectConfig !== undefined) {
			ZenoService.addTag($projectConfig.uuid, {
				id: 0,
				tagName,
				items: []
			}).then(() => {
				if ($projectConfig !== undefined) {
					ZenoService.getTags($projectConfig.uuid).then((fetchedTags) => {
						tags.set(fetchedTags);
						showNewTag.set(false);
					});
				}
			});
		}
	}

	function submit(e) {
		if ($showNewTag && e.key === 'Escape') {
			showNewTag.set(false);
		}
		if ($showNewTag && e.key === 'Enter') {
			createTag();
		}
	}
</script>

<svelte:window on:keydown={submit} />

<div id="paper-container" use:clickOutside on:clickOutside={() => showNewTag.set(false)}>
	<Paper elevation={7}>
		<Content style="display: flex; align-items: center;">
			<Textfield bind:value={tagName} label="Tag Name" bind:this={input} />
			<Button style="margin-left: 10px;" variant="outlined" on:click={() => showNewTag.set(false)}
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
	</Paper>
</div>

<style>
	#paper-container {
		position: fixed;
		left: 440px;
		top: 70px;
		z-index: 20;
	}
</style>
