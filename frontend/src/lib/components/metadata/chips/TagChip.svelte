<script lang="ts">
	import { TrailingIcon } from '@smui/chips';

	import { selections, tagIds, tags } from '$lib/stores';

	export let tagId: number;

	function cancelClicked() {
		selections.update((sel) => {
			sel.tags.splice(sel.tags.indexOf(tagId), 1);
			return { slices: sel.slices, metadata: sel.metadata, tags: sel.tags };
		});

		let s = new Set<string>();
		//this is to catch for the case when you have intersections between tags
		//must come after selections is updated
		$selections.tags.forEach((currId) => {
			const current = $tags.find((tag) => tag.id === currId);
			if (current) {
				current.dataIds.forEach((item) => s.add(item));
			}
		});
		tagIds.set([...s]);
	}
</script>

<div class="mr-1 w-fit rounded bg-greenish-light px-2.5 py-1">
	{$tags.find((tag) => tag.id === tagId)?.tagName}
	<TrailingIcon class="remove material-icons" on:click={cancelClicked}>cancel</TrailingIcon>
</div>
