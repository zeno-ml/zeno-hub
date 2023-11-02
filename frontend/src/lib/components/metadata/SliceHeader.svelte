<script lang="ts">
	import { page } from '$app/stores';
	import { models, project, selectionPredicates, selections } from '$lib/stores';
	import { tooltip } from '$lib/util/tooltip';
	import {
		mdiCreation,
		mdiCreationOutline,
		mdiFolderPlusOutline,
		mdiInformationOutline,
		mdiPlus,
		mdiPlusCircle
	} from '@mdi/js';
	import IconButton, { Icon } from '@smui/icon-button';
	import FolderPopup from '../popups/FolderPopup.svelte';
	import SliceFinderPopup from '../popups/SliceFinderPopup.svelte';
	import SlicePopup from '../popups/SlicePopup.svelte';

	let showSliceFinder = false;
	let showNewFolder = false;
	let showNewSlice = false;
</script>

{#if showSliceFinder}
	<SliceFinderPopup on:close={() => (showSliceFinder = false)} />
{/if}
{#if showNewSlice}
	<SlicePopup on:close={() => (showNewSlice = false)} />
{/if}
{#if showNewFolder}
	<FolderPopup on:close={() => (showNewFolder = false)} />
{/if}
<div
	class="sticky {$models.length > 0
		? 'top-16'
		: '-top-2'} z-10 flex min-h-[40px] items-center justify-between bg-yellowish-light"
>
	<div class="flex items-center justify-between">
		<h4>Slices</h4>
		<div
			class="h-6 w-6 cursor-help fill-grey-dark"
			use:tooltip={{
				text: 'Slices are named combinations of filters'
			}}
		>
			<Icon style="outline:none" tag="svg" viewBox="-6 -6 36 36">
				<path d={mdiInformationOutline} />
			</Icon>
		</div>
	</div>
	{#if $project.editor}
		<div class="flex items-center justify-between">
			<div
				use:tooltip={{
					text: !$page.url.href.includes('compare')
						? 'Find underperforming slices'
						: 'Find slices with the largest output differences between systems'
				}}
			>
				<IconButton
					on:click={() => {
						showSliceFinder = true;
					}}
				>
					<Icon tag="svg" viewBox="0 0 24 24">
						{#if $selectionPredicates !== undefined || $selections.tags.length > 0}
							<path class="fill-primary" d={mdiCreation} />
						{:else}
							<path class="fill-grey" d={mdiCreationOutline} />
						{/if}
					</Icon>
				</IconButton>
			</div>
			<div
				use:tooltip={{
					text: 'Create a new folder'
				}}
			>
				<IconButton
					on:click={() => {
						showNewFolder = true;
					}}
				>
					<Icon tag="svg" viewBox="0 0 24 24">
						<path class="fill-grey" d={mdiFolderPlusOutline} />
					</Icon>
				</IconButton>
			</div>
			<div
				use:tooltip={{
					text: 'Create a new slice'
				}}
			>
				<IconButton
					on:click={() => {
						showNewSlice = true;
					}}
				>
					<Icon tag="svg" viewBox="0 0 24 24">
						{#if $selectionPredicates !== undefined}
							<path class="fill-primary" d={mdiPlusCircle} />
						{:else}
							<path class="fill-grey" d={mdiPlus} />
						{/if}
					</Icon>
				</IconButton>
			</div>
		</div>
	{/if}
</div>
