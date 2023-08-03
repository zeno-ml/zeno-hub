<script lang="ts">
	export let entry: Record<string, number | string | boolean>;
	export let modelColumn: string;

	$: imageURL = entry['data'] as string;
</script>

<div class="w-min p-2 border border-grey-lighter" style:background-color="white">
	<img src={imageURL} style:max-width="200px" alt="Image thumbnail for instance {entry['item']}" />
	<br />
	<div class="flex">
		<span class="mr-2 text-xs">label: </span>
		<span class="value text-xs">{entry['label']}</span>
	</div>
	{#if modelColumn && entry[modelColumn]}
		<div class="flex">
			<span class="mr-2 text-xs">output: </span>
			<span class="value text-xs">{entry[modelColumn]} </span>
		</div>
	{/if}
</div>
