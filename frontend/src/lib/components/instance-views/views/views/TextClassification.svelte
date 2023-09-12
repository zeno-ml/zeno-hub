<script lang="ts">
	import { resolveDataPoint } from '$lib/util/util';
	import CircularProgress from '@smui/circular-progress/src/CircularProgress.svelte';

	// Objects with keys corresponding to the following props.
	export let entry: Record<string, string | number | boolean>;
	// Key for model outputs.
	export let modelColumn: string;
</script>

<div class="p-4 border border-grey-lighter max-w-[450px] min-w-[400px] rounded break-words">
	{#await resolveDataPoint(entry)}
		<CircularProgress style="height: 32px; width: 32px; margin-right:20px" indeterminate />
	{:then textData}
		<p class="text-grey">
			<span class="font-semibold">input: </span>
			{textData}
		</p>
	{/await}
	{#if entry['label'] !== undefined}
		<p class="mt-2 text-grey">
			<span class="font-semibold">label: </span>
			{entry['label']}
		</p>
	{/if}
	{#if modelColumn && entry[modelColumn] !== undefined}
		<hr class="mt-2 mb-2 text-grey-darker" />
		<p class=" text-grey">
			<span class="font-semibold">output: </span>
			{entry[modelColumn]}
		</p>
	{/if}
</div>
