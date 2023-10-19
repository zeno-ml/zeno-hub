<script lang="ts">
	import { page } from '$app/stores';
	import { editTag, editedIds, project, selectionIds, selections, tagIds, tags } from '$lib/stores';
	import type { Tag, ZenoService } from '$lib/zenoapi';
	import { mdiInformationOutline, mdiPlus, mdiPlusCircle } from '@mdi/js';
	import Button from '@smui/button';
	import IconButton, { Icon } from '@smui/icon-button';
	import { tooltip } from '@svelte-plugins/tooltips';
	import { getContext } from 'svelte';
	import TagPopup from '../popups/TagPopup.svelte';
	import TagCell from './cells/TagCell.svelte';

	const zenoClient = getContext('zenoClient') as ZenoService;

	let showNewTag = false;

	function saveChanges() {
		if ($editTag === undefined) return;
		zenoClient
			.updateTag($project.uuid, {
				...$editTag,
				dataIds: Array.from(new Set([...$editTag.dataIds, ...$editedIds]))
			})
			.then(() => {
				tags.update((t) => {
					const index = t.findIndex((tag) => tag.id === $editTag?.id);
					if (index !== -1 && $editTag !== undefined) {
						t[index] = { ...$editTag, dataIds: $editedIds };
					}
					return t;
				});
				let s = new Set<string>();
				$selections.tags.forEach((tagId) => {
					const tag: Tag | undefined = $tags.find((cur) => cur.id === tagId);
					if (tag !== undefined) tag.dataIds.forEach((item) => s.add(item));
					tagIds.set([...s]);
				});
				editTag.set(undefined);
				editedIds.set([]);
			});
	}
</script>

{#if showNewTag}
	<TagPopup on:close={() => (showNewTag = false)} />
{/if}
<div class="flex items-center justify-between mt-4">
	<div class="flex items-center justify-between">
		<h4>Tags</h4>
		<div
			class="w-6 h-6 cursor-help fill-grey-darker"
			use:tooltip={{
				content: 'Tags are named sets of data instances',
				position: 'right',
				theme: 'zeno-tooltip'
			}}
		>
			<Icon tag="svg" viewBox="-6 -6 36 36">
				<path d={mdiInformationOutline} />
			</Icon>
		</div>
	</div>
	{#if $project.editor && !$page.url.href.includes('compare')}
		<div class="flex items-center justify-between">
			<div
				use:tooltip={{
					content: 'Create a new tag',
					position: 'left',
					theme: 'zeno-tooltip'
				}}
			>
				<IconButton on:click={() => (showNewTag = true)}>
					<Icon tag="svg" viewBox="0 0 24 24">
						{#if $selectionIds !== undefined}
							<path class="fill-greenish" d={mdiPlusCircle} />
						{:else}
							<path class="fill-grey" d={mdiPlus} />
						{/if}
					</Icon>
				</IconButton>
			</div>
		</div>
	{/if}
</div>

<div class="mb-2">
	{#each [...$tags.values()] as t}
		{#if $editTag !== undefined && $editTag.id === t.id}
			<div style="display: flex; align-items: center">
				<div class="mr-2 w-full">
					<TagCell tag={t} />
				</div>
				<Button
					style="background-color: var(--N1); margin-top: 5px; color: white; "
					on:click={saveChanges}
				>
					Done
				</Button>
			</div>
		{:else}
			<TagCell tag={t} />
		{/if}
	{/each}
</div>
