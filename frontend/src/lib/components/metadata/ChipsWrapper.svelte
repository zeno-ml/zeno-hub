<script lang="ts">
	import { project, selectionIds, selectionPredicates, selections, tagIds } from '$lib/stores';
	import { Join, type FilterPredicate } from '$lib/zenoapi';
	import Button from '@smui/button';
	import SlicePopup from '../popups/SlicePopup.svelte';
	import IdsChip from './chips/IdsChip.svelte';
	import MetadataChip from './chips/MetadataChip.svelte';
	import SliceChip from './chips/SliceChip.svelte';
	import TagChip from './chips/TagChip.svelte';

	$: filters = Object.entries($selections.metadata)
		.filter(([, value]) => value.predicates.length > 0)
		.map(([key, value]) => [key, value.predicates as unknown] as [string, FilterPredicate[]]);

	let showNewSlice = false;
</script>

{#if showNewSlice}
	<SlicePopup on:close={() => (showNewSlice = false)} />
{/if}
<div class="flex flex-wrap height-fit items-center py-1">
	{#if $selections.slices.length + $selections.tags.length + filters.length === 0 && $selectionIds === undefined}
		<p style="margin: 0px">
			Filter by selecting slices or interacting with the feature distribution charts.
		</p>
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
			{#if $project.editor}
				<Button
					variant="outlined"
					class="ml-2"
					on:keydown={() => ({})}
					on:click={() => {
						showNewSlice = true;
					}}
				>
					create slice
				</Button>
			{/if}
			<Button
				variant="outlined"
				class="ml-2"
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
			</Button>
		{/if}
	{/if}
</div>
