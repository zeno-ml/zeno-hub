<script lang="ts">
	import InstanceView from '$lib/components/instance-views/InstanceView.svelte';

	export let data;
</script>

<div class="mx-5 flex flex-col flex-grow">
	<InstanceView compare={data.compare} />
</div>
