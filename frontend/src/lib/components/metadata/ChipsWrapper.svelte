<script lang="ts">
	import { filterSelection, project, selectionPredicates, selections, tagIds } from '$lib/stores';
	import { Join, type FilterPredicate } from '$lib/zenoapi';
	import Button from '@smui/button';
	import SlicePopup from '../popups/SlicePopup.svelte';
	import MetadataChip from './chips/MetadataChip.svelte';
	import SliceChip from './chips/SliceChip.svelte';
	import TagChip from './chips/TagChip.svelte';

	let showNewSlice = false;

	$: filters = Object.entries($selections.metadata)
		.filter(([, value]) => value.predicates.length > 0)
		.map(([key, value]) => [key, value.predicates as unknown] as [string, FilterPredicate[]]);
</script>

{#if showNewSlice}
	<SlicePopup on:close={() => (showNewSlice = false)} />
{/if}
<div class="flex w-full flex-wrap items-center py-1">
	{#if $selections.slices.length + $selections.tags.length + filters.length === 0}
		<p>Filter by selecting slices or interacting with the feature distribution charts.</p>
	{:else}
		{#each $selections.slices as sliceIdx}
			<SliceChip {sliceIdx} />
		{/each}
		{#each filters as [hash, chip]}
			<MetadataChip {hash} {chip} />
		{/each}
		{#if $project.editor && $selectionPredicates !== undefined}
			<Button
				class="ml-1 mr-2"
				variant="outlined"
				on:keydown={() => ({})}
				on:click={() => {
					showNewSlice = true;
				}}
			>
				create slice
			</Button>
		{/if}
		{#each $selections.tags as tagId}
			<TagChip {tagId} />
		{/each}
		<Button
			variant="outlined"
			class="ml-1"
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
				tagIds.set(undefined);
				filterSelection.set(false);
			}}
		>
			clear all
		</Button>
	{/if}
</div>
