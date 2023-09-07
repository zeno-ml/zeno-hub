<script lang="ts">
	import InstanceView from '$lib/components/instance-views/InstanceView.svelte';
	import { model } from '$lib/stores.js';

	export let data;

	$: console.log($model);
</script>

<div class="mx-5 flex flex-col flex-grow w-1">
	<InstanceView compare={data.compare} />
</div>
