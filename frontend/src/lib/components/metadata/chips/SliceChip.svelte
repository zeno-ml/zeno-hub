<script lang="ts">
	import { TrailingIcon } from '@smui/chips';

	import { selections, slices } from '$lib/stores';

	export let sliceIdx: number;

	$: slice = $slices.find((slice) => slice.id === sliceIdx);
</script>

<div class="px-2.5 py-1 bg-primary-light mx-1 my rounded w-fit">
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
