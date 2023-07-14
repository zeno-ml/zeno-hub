<script lang="ts">
	import { TrailingIcon } from '@smui/chips';

	import { selections, slices } from '$lib/stores';

	export let sliceIdx: number;

	$: slice = $slices.find((slice) => slice.id === sliceIdx);
</script>

<div class="meta-chip">
	{slice !== undefined ? slice.sliceName : ''}
	<TrailingIcon
		class="remove material-icons"
		on:click={() =>
			selections.update((sel) => {
				sel.slices.splice(sel.slices.indexOf(sliceIdx), 1);
				return { slices: sel.slices, metadata: sel.metadata, tags: sel.tags };
			})}
	>
		cancel
	</TrailingIcon>
</div>

<style>
	.meta-chip {
		padding: 5px 10px;
		background: var(--P3);
		margin-left: 5px;
		margin-right: 5px;
		margin-top: 2px;
		margin-bottom: 2px;
		border-radius: 4px;
		width: fit-content;
	}
</style>
