<script lang="ts">
	import Histograms from './Histograms.svelte';
	import MetadataHeader from './MetadataHeader.svelte';
	import Slices from './Slices.svelte';
	import Tags from './Tags.svelte';
</script>

<div class="side-container">
	<MetadataHeader />
	<Slices />
	<Tags />
	<Histograms />
</div>

<style>
	.side-container {
		height: calc(100vh - 65px);
		width: 360px;
		min-width: 360px;
		max-width: 360px;
		padding-top: 10px;
		padding-bottom: 50px;
		padding-left: 15px;
		padding-right: 10px;
		overflow-y: scroll;
		background-color: var(--Y2);
	}
</style>
