<script lang="ts">
	import { selectionIds, selectionPredicates, selections, tagIds } from '$lib/stores';
	import { Join, type FilterPredicate } from '$lib/zenoapi';
	import IdsChip from './chips/IdsChip.svelte';
	import MetadataChip from './chips/MetadataChip.svelte';
	import SliceChip from './chips/SliceChip.svelte';
	import TagChip from './chips/TagChip.svelte';

	$: filters = Object.entries($selections.metadata)
		.filter(([, value]) => value.predicates.length > 0)
		.map(([key, value]) => [key, value.predicates as unknown] as [string, FilterPredicate[]]);
</script>

<div class="flex flex-wrap height-fit items-center py-1">
	{#if $selections.slices.length + $selections.tags.length + filters.length === 0 && $selectionIds === undefined}
		<p style="margin: 0px">Filter with the selected predicates.</p>
	{:else}
		{#each $selections.slices as sliceIdx}
			<SliceChip {sliceIdx} />
		{/each}
		{#each filters as [hash, chip]}
			<MetadataChip {hash} {chip} />
		{/each}
		{#each $selections.tags as tagId}
			<TagChip {tagId} />
		{/each}
		{#if $selectionIds !== undefined}
			<IdsChip />
		{/if}
		{#if $selectionPredicates !== undefined || $tagIds !== undefined || $selectionIds !== undefined}
			<span
				class="p-1 ml-2.5 cursor-pointer hover:bg-yellowish hover:rounded"
				on:keydown={() => ({})}
				on:click={() => {
					selections.update((m) => {
						Object.keys(m.metadata).forEach((key) => {
							m.metadata[key] = {
								predicates: [],
								join: Join._
							};
						});
						return { slices: [], metadata: { ...m.metadata }, tags: [] };
					});
					selectionIds.set(undefined);
					tagIds.set(undefined);
				}}
			>
				clear all
			</span>
		{/if}
	{/if}
</div>
