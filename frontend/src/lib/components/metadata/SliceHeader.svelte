<script lang="ts">
	import { page } from '$app/stores';
	import { selectionIds, selectionPredicates, selections } from '$lib/stores';
	import {
		mdiCreation,
		mdiCreationOutline,
		mdiFolderPlusOutline,
		mdiInformationOutline,
		mdiPlus,
		mdiPlusCircle
	} from '@mdi/js';
	import IconButton, { Icon } from '@smui/icon-button';
	import { tooltip } from '@svelte-plugins/tooltips';
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
<div class="sticky top-14 bg-yellowish-light flex items-center justify-between z-10">
	<div class="flex items-center justify-between">
		<h4>Slices</h4>
		<div
			class="w-6 h-6 cursor-help fill-grey-dark"
			use:tooltip={{
				content: 'Slices are named combinations of filters.',
				position: 'right',
				theme: 'zeno-tooltip'
			}}
		>
			<Icon style="outline:none" tag="svg" viewBox="-6 -6 36 36">
				<path d={mdiInformationOutline} />
			</Icon>
		</div>
	</div>
	<div class="flex items-center justify-between">
		<div
			use:tooltip={{
				content: !$page.url.href.includes('compare')
					? 'Find underperforming slices.'
					: 'Find slices with the largest output differences between models',
				position: 'left',
				theme: 'zeno-tooltip',
				maxWidth: '150'
			}}
		>
			<IconButton
				on:click={() => {
					showSliceFinder = true;
				}}
			>
				<Icon tag="svg" viewBox="0 0 24 24">
					{#if $selectionPredicates !== undefined || $selections.tags.length > 0 || ($selectionIds !== undefined && $selectionIds.length > 0)}
						<path class="fill-primary" d={mdiCreation} />
					{:else}
						<path class="fill-grey" d={mdiCreationOutline} />
					{/if}
				</Icon>
			</IconButton>
		</div>
		<div
			use:tooltip={{
				content: 'Create a new folder.',
				position: 'left',
				theme: 'zeno-tooltip'
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
				content: 'Create a new slice.',
				position: 'left',
				theme: 'zeno-tooltip'
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
</div>
