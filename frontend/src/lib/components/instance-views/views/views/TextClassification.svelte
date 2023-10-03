<script lang="ts">
	import { resolveDataPoint } from '$lib/util/util';
	import CircularProgress from '@smui/circular-progress/src/CircularProgress.svelte';

	// Objects with keys corresponding to the following props.
	export let entry: Record<string, string | number | boolean>;
	export let dataColumn: string;
	export let labelColumn: string;
	export let modelColumn: string;
</script>

<div class="p-4 border border-grey-lighter max-w-[450px] min-w-[400px] rounded break-words">
	{#await resolveDataPoint(entry[dataColumn])}
		<CircularProgress style="height: 32px; width: 32px; margin-right:20px" indeterminate />
	{:then textData}
		<p class="text-grey whitespace-pre-wrap">
			<span class="font-semibold">input: </span>
			{textData}
		</p>
	{/await}
	{#if entry[labelColumn] !== undefined}
		<p class="mt-2 text-grey whitespace-pre-wrap">
			<span class="font-semibold">label: </span>
			{entry[labelColumn]}
		</p>
	{/if}
	{#if modelColumn && entry[modelColumn] !== undefined}
		<hr class="mt-2 mb-2 text-grey-darker" />
		<p class=" text-grey whitespace-pre-wrap">
			<span class="font-semibold">output: </span>
			{entry[modelColumn]}
		</p>
	{/if}
</div>
