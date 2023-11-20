<script lang="ts">
	import Spinner from '$lib/components/general/Spinner.svelte';

	export let chartName: string;
	export let loading = false;
</script>

<div class="ml-5 mt-5">
	<div class="mb-3 mt-2 flex items-center">
		<h2 class="mr-2 text-xl text-grey-dark">
			{chartName}
		</h2>
		{#if loading}
			<Spinner width={24} height={24} />
		{/if}
	</div>
	<div>
		<slot />
	</div>
</div>
