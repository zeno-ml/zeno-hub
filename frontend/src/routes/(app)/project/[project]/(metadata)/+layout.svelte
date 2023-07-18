<script lang="ts">
	import MetadataPanel from '$lib/components/metadata/MetadataPanel.svelte';
	import NewFolderPopup from '$lib/components/metadata/popups/NewFolderPopup.svelte';
	import NewSlicePopup from '$lib/components/metadata/popups/NewSlicePopup.svelte';
	import NewTagPopup from '$lib/components/metadata/popups/NewTagPopup.svelte';
	import SliceFinderPopup from '$lib/components/metadata/popups/SliceFinderPopup.svelte';
	import {
		projectConfig,
		showNewFolder,
		showNewSlice,
		showNewTag,
		showSliceFinder
	} from '$lib/stores';
</script>

<!-- These popups are at the top level b/c of issues with overflow-y scroll. -->
{#if $showNewSlice && $projectConfig}
	<NewSlicePopup />
{/if}
{#if $showNewFolder}
	<NewFolderPopup />
{/if}
{#if $showSliceFinder}
	<SliceFinderPopup />
{/if}
{#if $showNewTag}
	<NewTagPopup />
{/if}
<div class="container">
	<MetadataPanel />
	<slot />
</div>

<style>
	.container {
		display: flex;
		flex-direction: row;
		flex-grow: 1;
	}
</style>
