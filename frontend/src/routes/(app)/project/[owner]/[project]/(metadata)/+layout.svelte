<script lang="ts">
	import MetadataPanel from '$lib/components/metadata/MetadataPanel.svelte';
	import { decodeURLParameters } from '$lib/util/util';

	decodeURLParameters();
</script>

<MetadataPanel />
<slot />
