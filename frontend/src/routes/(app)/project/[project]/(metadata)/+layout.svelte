<script lang="ts">
	import MetadataPanel from '$lib/components/metadata/MetadataPanel.svelte';
</script>

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
