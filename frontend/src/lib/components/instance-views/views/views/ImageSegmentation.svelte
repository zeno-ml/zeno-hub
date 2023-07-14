<script lang="ts">
	// List of objects with keys corresponding to the following props.
	export let entry;
	export let viewOptions;
	// Key for model outputs.
	export let modelColumn;
	// Key for groundtruth labels.
	export let labelColumn;
	// Key for the input data.
	export let dataColumn;
	// Key for unique identifier of each item.
	export let idColumn;
</script>

<div class="box">
	<div id="overlays">
		<img
			src={entry[dataColumn]}
			style:width="150px"
			style:height="150px"
			alt="Image thumbnail for instance {entry[idColumn]}"
		/>
		{#if viewOptions['mask'].includes('Label')}
			<img
				class="overlay"
				src="/labels/{entry[labelColumn]}"
				style:width="150px"
				style:height="150px"
				alt="Image thumbnail for instance {entry[labelColumn]}"
			/>
		{/if}
		{#if entry[modelColumn] && viewOptions['mask'].includes('Model')}
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
