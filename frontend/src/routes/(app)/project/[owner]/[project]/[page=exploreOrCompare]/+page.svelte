<script lang="ts">
	import InstanceView from '$lib/components/instance-views/InstanceView.svelte';
	import MetadataPanel from '$lib/components/metadata/MetadataPanel.svelte';

	export let data;
</script>

<MetadataPanel compare={data.compare} />
<div class="mx-5 flex flex-col flex-grow w-1">
	<InstanceView compare={data.compare} />
</div>
