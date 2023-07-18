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
	import { Svg } from '@smui/common';
	import IconButton, { Icon } from '@smui/icon-button';
	import { tooltip } from '@svelte-plugins/tooltips';
	import FolderPopup from './popups/FolderPopup.svelte';
	import Popup from './popups/Popup.svelte';
	import SliceFinderPopup from './popups/SliceFinderPopup.svelte';
	import SlicePopup from './popups/SlicePopup.svelte';

	let showSliceFinder = false;
	let showNewFolder = false;
	let showNewSlice = false;
</script>

{#if showSliceFinder}
	<Popup on:close={() => (showSliceFinder = false)}>
		<SliceFinderPopup on:close={() => (showSliceFinder = false)} />
	</Popup>
{/if}
{#if showNewSlice}
	<Popup on:close={() => (showNewSlice = false)}>
		<SlicePopup on:close={() => (showNewSlice = false)} />
	</Popup>
{/if}
{#if showNewFolder}
	<Popup on:close={() => (showNewFolder = false)}>
		<FolderPopup on:close={() => (showNewFolder = false)} />
	</Popup>
{/if}
<div class="slice-header inline">
	<div class="inline">
		<h4>Slices</h4>
		<div
			class="information-tooltip"
			use:tooltip={{
				content: 'Slices are named combinations of filters.',
				position: 'right',
				theme: 'zeno-tooltip'
			}}
		>
			<Icon style="outline:none" component={Svg} viewBox="-6 -6 36 36">
				<path d={mdiInformationOutline} />
			</Icon>
		</div>
	</div>
	<div class="inline">
		<div
			use:tooltip={{
				content: !$page.url.href.includes('compare')
					? 'Find underperforming slices.'
					: 'Find slices with the largest output differences between models',
				position: 'left',
				theme: 'zeno-tooltip',
				maxWidth: !$page.url.href.includes('compare') ? '150' : '200'
			}}
		>
			<IconButton
				on:click={() => {
					showSliceFinder = true;
				}}
			>
				<Icon component={Svg} viewBox="0 0 24 24">
					{#if $selectionPredicates !== undefined || $selections.tags.length > 0 || ($selectionIds !== undefined && $selectionIds.length > 0)}
						<path fill="#6a1a9a" d={mdiCreation} />
					{:else}
						<path fill="var(--G1)" d={mdiCreationOutline} />
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
				<Icon component={Svg} viewBox="0 0 24 24">
					<path fill="var(--G1)" d={mdiFolderPlusOutline} />
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
				<Icon component={Svg} viewBox="0 0 24 24">
					{#if $selectionPredicates !== undefined}
						<path fill="#6a1a9a" d={mdiPlusCircle} />
					{:else}
						<path fill="var(--G1)" d={mdiPlus} />
					{/if}
				</Icon>
			</IconButton>
		</div>
	</div>
</div>

<style>
	.slice-header {
		position: sticky;
		top: 60px;
		z-index: 3;
		background-color: var(--Y2);
	}

	.inline {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
</style>
