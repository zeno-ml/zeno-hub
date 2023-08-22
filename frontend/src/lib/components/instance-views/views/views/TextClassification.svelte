<script lang="ts">
	import { resolveDataPoint } from '$lib/util/util';
	import CircularProgress from '@smui/circular-progress/src/CircularProgress.svelte';

	// Objects with keys corresponding to the following props.
	export let entry: Record<string, string | number | boolean>;
	// Key for model outputs.
	export let modelColumn: string;
</script>

<div class="p-2.5 border border-grey-lighter">
	{#await resolveDataPoint(entry)}
		<CircularProgress style="height: 32px; width: 32px; margin-right:20px" indeterminate />
	{:then textData}
		<span>{textData}</span>
	{/await}
	<br />
	{#if entry['label'] !== undefined}
		<span class="text-xs">label: </span>
		<span class="text-xs">
			{entry['label']}
		</span>
	{/if}
	{#if modelColumn && entry[modelColumn] !== undefined}
		<br />
		<span class="text-xs">output: </span>
		<span class="text-xs">{entry[modelColumn]} </span>
	{/if}
</div>
