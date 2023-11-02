<script lang="ts">
	import { collapseHeader, models } from '$lib/stores';
	import Histograms from './Histograms.svelte';
	import HistogramsHeader from './HistogramsHeader.svelte';
	import MetadataHeader from './MetadataHeader.svelte';
	import Slices from './Slices.svelte';
	import Tags from './Tags.svelte';

	export let compare = false;
</script>

<div
	class="h-full w-[380px] shrink-0 overflow-y-auto border-r border-r-grey-lighter bg-yellowish-light px-5 pb-5 pt-2 {$collapseHeader
		? 'hide-sidebar'
		: 'show-sidebar'}"
>
	{#if $models.length > 0}
		<MetadataHeader />
	{/if}
	<Slices />
	<Tags />
	{#if !compare}
		<HistogramsHeader />
		<Histograms />
	{/if}
</div>

<style>
	div {
		transition: all 0.5s ease-in-out;
	}
	.show-sidebar {
		visibility: visible;
	}

	.hide-sidebar {
		visibility: none;
		margin-left: -380px;
	}
</style>
