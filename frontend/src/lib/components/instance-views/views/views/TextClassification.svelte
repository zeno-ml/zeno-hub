<script lang="ts">
	// Objects with keys corresponding to the following props.
	export let entry: Record<string, string | number | boolean>;
	// Key for model outputs.
	export let modelColumn: string;

	$: textData = entry['data'] as string;
</script>

<div class="p-2.5 border border-grey-lighter">
	<span>{textData}</span>
	<br />
	<span class="text-xs">label: </span>
	<span class="text-xs">
		{entry['label']}
	</span>
	{#if modelColumn && entry[modelColumn] !== undefined}
		<br />
		<span class="text-xs">output: </span>
		<span class="text-xs">{entry[modelColumn]} </span>
	{/if}
</div>
