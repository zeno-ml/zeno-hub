<script lang="ts">
	import { collapseHeader } from '$lib/stores';
	import Histograms from './Histograms.svelte';
	import HistogramsHeader from './HistogramsHeader.svelte';
	import MetadataHeader from './MetadataHeader.svelte';
	import Slices from './Slices.svelte';
	import Tags from './Tags.svelte';

	export let compare = false;
</script>

<div
	class="h-full p-5 overflow-y-auto shrink-0 bg-yellowish-light w-[380px] {$collapseHeader
		? 'hide-sidebar'
		: 'show-sidebar'}"
>
	<MetadataHeader />
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
