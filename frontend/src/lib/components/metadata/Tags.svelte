<script lang="ts">
	import { page } from '$app/stores';
	import {
		editTag,
		editedIds,
		projectConfig,
		selectionIds,
		selections,
		tagIds,
		tags
	} from '$lib/stores';
	import { ZenoService } from '$lib/zenoapi';
	import { mdiInformationOutline, mdiPlus, mdiPlusCircle } from '@mdi/js';
	import Button from '@smui/button';
	import IconButton, { Icon } from '@smui/icon-button';
	import { tooltip } from '@svelte-plugins/tooltips';
	import TagPopup from '../popups/TagPopup.svelte';
	import TagCell from './cells/TagCell.svelte';

	let showNewTag = false;

	function saveChanges() {
		if ($editTag === undefined || $projectConfig === undefined) return;
		ZenoService.updateTag($projectConfig.uuid, { ...$editTag, items: $editedIds }).then(() => {
			editTag.set(undefined);
			editedIds.set([]);
			if ($projectConfig !== undefined) {
				ZenoService.getTags($projectConfig.uuid).then((fetchedTags) => {
					tags.set(fetchedTags);
					let s = new Set<string>();
					$selections.tags.forEach((tagId) => {
						const tag = $tags.find((cur) => cur.id === tagId);
						if (tag !== undefined) tag.items.forEach((item) => s.add(item));
						tagIds.set([...s]);
					});
				});
			}
		});
	}
</script>

{#if showNewTag}
	<TagPopup on:close={() => (showNewTag = false)} />
{/if}
<div class=" flex items-center justify-between" style:margin-top="10px">
	<div class="flex items-center justify-between">
		<h4>Tags</h4>
		<div
			class="w-6 h-6 cursor-help fill-grey-darker"
			use:tooltip={{
				content: 'Tags are named sets of data instances.',
				position: 'right',
				theme: 'zeno-tooltip'
			}}
		>
			<Icon tag="svg" viewBox="-6 -6 36 36">
				<path d={mdiInformationOutline} />
			</Icon>
		</div>
	</div>
	{#if !$page.url.href.includes('compare')}
		<div class="flex items-center justify-between">
			<div>
				<div
					use:tooltip={{
						content: 'Create a new tag.',
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
		</div>
	{/if}
</div>

{#each [...$tags.values()] as t}
	{#if $editTag !== undefined && $editTag.id === t.id}
		<div style="display: flex; align-items: center">
			<div style="width: 100%; margin-right: 10px">
				<TagCell tag={t} />
			</div>
			<Button
				style="background-color: var(--N1); margin-top: 5px; color: white; "
				on:click={saveChanges}>Done</Button
			>
		</div>
	{:else}
		<TagCell tag={t} />
	{/if}
{/each}
