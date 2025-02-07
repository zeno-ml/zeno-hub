<script lang="ts">
	import { page } from '$app/stores';
	import Confirm from '$lib/components/popups/Confirm.svelte';
	import { folders, project, slices } from '$lib/stores';
	import { clickOutside } from '$lib/util/clickOutside';
	import type { Folder, ZenoService } from '$lib/zenoapi';
	import { mdiChevronDown, mdiChevronRight, mdiDotsHorizontal } from '@mdi/js';
	import Checkbox from '@smui/checkbox';
	import IconButton, { Icon } from '@smui/icon-button';
	import Paper, { Content } from '@smui/paper';
	import { getContext } from 'svelte';
	import { slide } from 'svelte/transition';
	import NewFolderPopup from '../../popups/FolderPopup.svelte';
	import SliceCell from './SliceCell.svelte';

	export let folder: Folder;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let editing = false;
	let expandFolder = false;
	let dragOver = false;
	let hovering = false;
	let showOptions = false;
	let showConfirmDelete = false;
	let deleteSlices = true;

	$: sls = $slices.filter((s) => s.folderId === folder.id);

	function dragDropped(ev: DragEvent) {
		dragOver = false;
		if (ev.dataTransfer) {
			const data = ev.dataTransfer.getData('text/plain').split(',');
			data.forEach((element) => {
				const slice = $slices.find((slice) => slice.id === parseInt(element));
				if (slice) {
					zenoClient
						.updateSlice($project.uuid, {
							...slice,
							folderId: folder.id
						})
						.then(() => {
							slices.update((s) => {
								const index = s.findIndex((s) => s.id === slice.id);
								if (index !== -1) {
									s[index] = { ...slice, folderId: folder.id };
								}
								return s;
							});
						});
				}
			});
		}
	}
</script>

{#if editing}
	<NewFolderPopup on:close={() => (editing = false)} folderToEdit={folder} />
{/if}
{#if showConfirmDelete}
	<Confirm
		message="Are you sure you want to delete this folder?"
		on:cancel={() => {
			showConfirmDelete = false;
			deleteSlices = true;
		}}
		on:confirm={() => {
			zenoClient.deleteFolder($project.uuid, folder.id, deleteSlices).then(() => {
				slices.update((s) => {
					if (deleteSlices) {
						s = s.filter((slice) => slice.folderId !== folder.id);
					} else {
						s.forEach((slice) => {
							if (slice.folderId === folder.id) {
								slice.folderId = undefined;
							}
						});
					}
					return s;
				});
				folders.update((f) => {
					const index = f.findIndex((f) => f.id === folder.id);
					if (index !== -1) {
						f.splice(index, 1);
					}
					return f;
				});
				showConfirmDelete = false;
				deleteSlices = true;
			});
		}}
	>
		<div class="flex items-center">
			<Checkbox bind:checked={deleteSlices} />
			<span>Delete contained slices</span>
		</div>
	</Confirm>
{/if}
<button
	class="relative mt-1 flex h-9 w-full items-center justify-between rounded bg-grey-lighter px-2.5 {dragOver
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
	<div class="flex min-w-0 items-center">
		<button
			class="shrink-0"
			style="width: 24px; height: 24px; cursor: pointer; margin-right: 10px;"
			on:keydown={() => ({})}
			on:click={() => (expandFolder = !expandFolder)}
		>
			<Icon style="outline:none" tag="svg" viewBox="0 0 24 24">
				<path fill="black" d={expandFolder ? mdiChevronDown : mdiChevronRight} />
			</Icon>
		</button>
		<span class="truncate">
			{folder.name}
		</span>
	</div>
	<div class="flex shrink-0 items-center pl-2" use:clickOutside={() => (showOptions = false)}>
		{#if showOptions}
			<div class="absolute right-0 top-0 z-10 mt-9">
				<Paper style="padding: 3px 0px;" elevation={7}>
					<Content>
						<button
							class="py flex w-20 cursor-pointer items-center px-2 hover:bg-grey-lighter"
							on:keydown={() => ({})}
							on:click={(e) => {
								e.stopPropagation();
								showOptions = false;
								editing = true;
							}}
						>
							<Icon style="font-size: 18px;" class="material-icons">edit</Icon>&nbsp;
							<span class="text-xs">Edit</span>
						</button>
						<button
							class="py flex w-20 cursor-pointer items-center px-2 hover:bg-grey-lighter"
							on:keydown={() => ({})}
							on:click={(e) => {
								e.stopPropagation();
								showOptions = false;
								showConfirmDelete = true;
							}}
						>
							<Icon style="font-size: 18px;" class="material-icons">delete_outline</Icon>&nbsp;
							<span class="text-xs">Remove</span>
						</button>
					</Content>
				</Paper>
			</div>
		{/if}
		<div style:margin-right="10px">
			{sls.length} slice{sls.length === 1 ? '' : 's'}
		</div>
		{#if $project.editor}
			<div class="flex items-center" style:cursor="pointer">
				<div style:width="36px">
					{#if hovering}
						<IconButton
							size="button"
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
		{/if}
	</div>
</button>
{#if expandFolder}
	<div transition:slide class="ml-9">
		{#each sls as s}
			<SliceCell compare={$page.url.href.includes('compare')} slice={s} />
		{/each}
	</div>
{/if}
