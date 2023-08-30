<script lang="ts">
	import { collapseHeader } from '$lib/stores';
	import Histograms from './Histograms.svelte';
	import MetadataHeader from './MetadataHeader.svelte';
	import Slices from './Slices.svelte';
	import Tags from './Tags.svelte';
</script>

<div
	class="h-full p-5 overflow-y-auto shrink-0 bg-yellowish-light w-[400px]"
	style:display={$collapseHeader ? 'none' : 'block'}
>
	<MetadataHeader />
	<Slices />
	<Tags />
	<Histograms />
</div>
