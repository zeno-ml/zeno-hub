<script lang="ts">
	import { resolveDataPoint } from '$lib/util/util';
	import CircularProgress from '@smui/circular-progress/src/CircularProgress.svelte';

	// List of objects with keys corresponding to the following props.
	export let entry: Record<string, number | string | boolean | { role: string; content: string }[]>;
	export let modelColumn: string;
	export let viewOptions: Record<string, unknown>;

	$: fetchImage = (async () => {
		const response = (await resolveDataPoint(entry)) as Response;
		return await response.blob();
	})();
	$: maskOption =
		viewOptions['mask'] && (viewOptions['mask'] as string).includes('Label') ? 'label' : 'model';
</script>

<div class="p-2.5 border border-grey-lighter">
	<div class="relative">
		{#await fetchImage}
			<CircularProgress style="height: 32px; width: 32px; margin-right:20px" indeterminate />
		{:then data}
			<img
				src={URL.createObjectURL(data)}
				style:width="150px"
				style:height="150px"
				alt="Image thumbnail for instance {entry['data_id']}"
			/>
		{/await}
		{#if maskOption === 'label'}
			<img
				class="absolute left-0 filter invert opacity-40"
				src="/labels/{entry['label']}"
				style:width="150px"
				style:height="150px"
				alt="Image thumbnail for instance {entry['label']}"
			/>
		{/if}
		{#if entry[modelColumn] && maskOption === 'model'}
			<img
				class="absolute left-0 filter invert opacity-40"
				src="/cache/{modelColumn}/{entry[modelColumn]}"
				style:width="150px"
				style:height="150px"
				alt="Image thumbnail for instance {entry[modelColumn]}"
			/>
		{/if}
	</div>
</div>
