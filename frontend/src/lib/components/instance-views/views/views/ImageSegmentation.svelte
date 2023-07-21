<script lang="ts">
	// List of objects with keys corresponding to the following props.
	export let entry: Record<string, number | string | boolean | { role: string; content: string }[]>;
	export let modelColumn: string;
	export let viewOptions: Record<string, unknown>;

	$: imageURL = entry['data'] as string;
	$: maskOption =
		viewOptions['mask'] && (viewOptions['mask'] as string).includes('Label') ? 'label' : 'model';
</script>

<div class="box">
	<div id="overlays">
		<img
			src={imageURL}
			style:width="150px"
			style:height="150px"
			alt="Image thumbnail for instance {entry['item']}"
		/>
		{#if maskOption === 'label'}
			<img
				class="overlay"
				src="/labels/{entry['label']}"
				style:width="150px"
				style:height="150px"
				alt="Image thumbnail for instance {entry['label']}"
			/>
		{/if}
		{#if entry[modelColumn] && maskOption === 'model'}
			<img
				class="overlay"
				src="/cache/{modelColumn}/{entry[modelColumn]}"
				style:width="150px"
				style:height="150px"
				alt="Image thumbnail for instance {entry[modelColumn]}"
			/>
		{/if}
	</div>
</div>

<style>
	#overlays {
		position: relative;
	}
	.overlay {
		filter: invert(100%) opacity(40%);
		left: 0px;
		position: absolute;
	}
	.box {
		padding: 10px;
		border: 0.5px solid rgb(224, 224, 224);
	}
</style>
