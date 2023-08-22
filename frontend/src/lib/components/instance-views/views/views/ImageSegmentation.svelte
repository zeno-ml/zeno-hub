<script lang="ts">
	// List of objects with keys corresponding to the following props.
	export let entry: Record<string, number | string | boolean | { role: string; content: string }[]>;
	export let modelColumn: string;
	export let viewOptions: Record<string, unknown>;

	$: imageURL = entry['data'] as string;
	$: maskOption =
		viewOptions['mask'] && (viewOptions['mask'] as string).includes('Label') ? 'label' : 'model';
</script>

<div class="p-2.5 border border-grey-lighter">
	<div class="relative">
		<img
			src={imageURL}
			style:width="150px"
			style:height="150px"
			alt="Image thumbnail for instance {entry['data_id']}"
		/>
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
