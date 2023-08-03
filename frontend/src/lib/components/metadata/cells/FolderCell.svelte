<script lang="ts">
	import { page } from '$app/stores';
	import { folders, projectConfig, slices } from '$lib/stores';
	import { clickOutside } from '$lib/util/clickOutside';
	import { ZenoService, type Folder } from '$lib/zenoapi';
	import { mdiChevronDown, mdiChevronRight, mdiDotsHorizontal } from '@mdi/js';
	import IconButton, { Icon } from '@smui/icon-button';
	import Paper, { Content } from '@smui/paper';
	import { slide } from 'svelte/transition';
	import NewFolderPopup from '../../popups/FolderPopup.svelte';
	import SliceCell from './SliceCell.svelte';

	export let folder: Folder;

	let editing = false;

	let expandFolder = false;
	let dragOver = false;

	let hovering = false;
	let showOptions = false;

	$: sls = $slices.filter((s) => s.folderId === folder.id);

	function dragDropped(ev: DragEvent) {
		dragOver = false;
		if (ev.dataTransfer) {
			const data = ev.dataTransfer.getData('text/plain').split(',');
			data.forEach((element) => {
				const slice = $slices.find((slice) => slice.id === parseInt(element));
				if (slice && $projectConfig) {
					ZenoService.updateSlice($projectConfig.uuid, {
						...slice,
						folderId: folder.id
					}).then(() => {
						if ($projectConfig) {
							ZenoService.getSlices($projectConfig.uuid).then((fetchedSlices) =>
								slices.set(fetchedSlices)
							);
						}
					});
				}
			});
		}
	}
</script>

{#if editing}
	<NewFolderPopup on:close={() => (editing = false)} folderToEdit={folder} />
{/if}
<div
	class="relative flex justify-between px-2.5 mt-1 rounded h-9 bg-grey-lighter {dragOver
		? 'bg-grey-light'
		: ''} {expandFolder ? 'mb-0' : ''}"
	on:mouseover={() => (hovering = true)}
	on:focus={() => (hovering = true)}
	on:mouseleave={() => (hovering = false)}
	on:blur={() => (hovering = false)}
	on:dragenter={() => (dragOver = true)}
	on:dragover={(ev) => ev.preventDefault()}
	on:dragleave={() => (dragOver = false)}
	on:drop={dragDropped}
>
	<div class="flex items-center">
		<div
			style="width: 24px; height: 24px; cursor: pointer; margin-right: 10px;"
			on:keydown={() => ({})}
			on:click={() => (expandFolder = !expandFolder)}
		>
			<Icon style="outline:none" tag="svg" viewBox="0 0 24 24">
				<path fill="black" d={expandFolder ? mdiChevronDown : mdiChevronRight} />
			</Icon>
		</div>
		{folder.name}
	</div>
	<div class="flex items-center" use:clickOutside={() => (showOptions = false)}>
		{#if showOptions}
			<div class="top-0 right-0 absolute mt-9">
				<Paper style="padding: 3px 0px;" elevation={7}>
					<Content>
						<div
							class="flex items-center cursor-pointer w-20 py px-2 hover:bg-grey-lighter"
							on:keydown={() => ({})}
							on:click={(e) => {
								e.stopPropagation();
								showOptions = false;
								editing = true;
							}}
						>
							<Icon style="font-size: 18px;" class="material-icons">edit</Icon>&nbsp;
							<span class="text-xs">Edit</span>
						</div>
						<div
							class="flex items-center cursor-pointer w-20 py px-2 hover:bg-grey-lighter"
							on:keydown={() => ({})}
							on:click={(e) => {
								e.stopPropagation();
								showOptions = false;
								ZenoService.deleteFolder(folder).then(() => {
									if ($projectConfig) {
										ZenoService.getSlices($projectConfig.uuid).then((fetchedSlices) =>
											slices.set(fetchedSlices)
										);
										ZenoService.getFolders($projectConfig.uuid).then((fetchedFolders) =>
											folders.set(fetchedFolders)
										);
									}
								});
							}}
						>
							<Icon style="font-size: 18px;" class="material-icons">delete_outline</Icon>&nbsp;
							<span class="text-xs">Remove</span>
						</div>
					</Content>
				</Paper>
			</div>
		{/if}
		<div style:margin-right="10px">
			{sls.length} slice{sls.length === 1 ? '' : 's'}
		</div>
		<div class="flex items-center" style:cursor="pointer">
			<div style:width="36px">
				{#if hovering}
					<IconButton
						size="button"
						style="padding: 0px"
						on:click={(e) => {
							e.stopPropagation();
							showOptions = !showOptions;
						}}
					>
						<Icon tag="svg" viewBox="0 0 24 24">
							<path fill="black" d={mdiDotsHorizontal} />
						</Icon>
					</IconButton>
				{/if}
			</div>
		</div>
	</div>
</div>
{#if expandFolder}
	<div transition:slide class="ml-9">
		{#each sls as s}
			<SliceCell compare={$page.url.href.includes('compare')} slice={s} />
		{/each}
	</div>
{/if}
