<script lang="ts">
	import {
		editTag,
		filterSelection,
		project,
		selectionIds,
		selectionPredicates,
		selections,
		tagIds,
		tags
	} from '$lib/stores';
	import { Join, ZenoService, type FilterPredicate, type Tag } from '$lib/zenoapi';
	import Button from '@smui/button';
	import { TrailingIcon } from '@smui/chips';
	import { getContext } from 'svelte';
	import SlicePopup from '../popups/SlicePopup.svelte';
	import TagPopup from '../popups/TagPopup.svelte';
	import MetadataChip from './chips/MetadataChip.svelte';
	import SliceChip from './chips/SliceChip.svelte';
	import TagChip from './chips/TagChip.svelte';

	const zenoClient = getContext('zenoClient') as ZenoService;

	let showNewSlice = false;
	let showNewTag = false;

	$: filters = Object.entries($selections.metadata)
		.filter(([, value]) => value.predicates.length > 0)
		.map(([key, value]) => [key, value.predicates as unknown] as [string, FilterPredicate[]]);

	function saveChanges() {
		if ($editTag === undefined) return;
		zenoClient
			.updateTag($project.uuid, {
				...$editTag,
				dataIds: $selectionIds
			})
			.then(() => {
				tags.update((t) => {
					const index = t.findIndex((tag) => tag.id === $editTag?.id);
					if (index !== -1 && $editTag !== undefined) {
						t[index] = { ...$editTag, dataIds: $selectionIds };
					}
					return t;
				});
				let s = new Set<string>();
				$selections.tags.forEach((tagId) => {
					const tag: Tag | undefined = $tags.find((cur) => cur.id === tagId);
					if (tag !== undefined) tag.dataIds.forEach((item) => s.add(item));
					tagIds.set([...s]);
				});
				editTag.set(undefined);
				selectionIds.set([]);
			});
	}
</script>

{#if showNewTag}
	<TagPopup on:close={() => (showNewTag = false)} />
{/if}
{#if showNewSlice}
	<SlicePopup on:close={() => (showNewSlice = false)} />
{/if}
<div class="flex w-full flex-wrap items-center py-1">
	{#if $selections.slices.length + $selections.tags.length + filters.length + $selectionIds.length === 0 && $editTag === undefined}
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
				class="mx-1"
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
		{#if $selectionIds.length > 0 || $editTag !== undefined}
			<div class="flex items-center">
				<button
					class="mx-1 flex w-fit rounded-2xl border-2 bg-greenish-light {$filterSelection
						? 'border-greenish'
						: 'border-greenish-light'} px-2.5 py-1"
					on:click={() => filterSelection.set(!$filterSelection)}
				>
					<span>{$selectionIds.length} instance{$selectionIds.length > 1 ? 's' : ''} selected</span>
					<TrailingIcon
						class="remove material-icons"
						on:click={() => {
							selectionIds.set([]);
							filterSelection.set(false);
						}}
					>
						cancel
					</TrailingIcon>
				</button>
				<Button
					variant="outlined"
					class="!text-greenish"
					on:keydown={() => ({})}
					on:click={() => {
						if ($editTag === undefined) showNewTag = true;
						else {
							saveChanges();
						}
					}}
				>
					{$editTag === undefined ? 'Create tag' : 'Update tag'}
				</Button>
			</div>
		{/if}
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
				selectionIds.set([]);
				filterSelection.set(false);
			}}
		>
			clear all
		</Button>
	{/if}
</div>
