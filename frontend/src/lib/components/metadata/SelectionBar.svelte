<script lang="ts">
	import { page } from '$app/stores';
	import {
		editTag,
		filterSelection,
		metric,
		project,
		selectionIds,
		selections,
		tagIds,
		tags
	} from '$lib/stores';
	import type { GroupMetric, Tag, ZenoService } from '$lib/zenoapi';
	import Button, { Group } from '@smui/button';
	import { TrailingIcon } from '@smui/chips';
	import { getContext } from 'svelte';
	import TagPopup from '../popups/TagPopup.svelte';
	import UpdateTagPopup from '../popups/UpdateTagPopup.svelte';
	import ChipsWrapper from './ChipsWrapper.svelte';

	export let currentResult: GroupMetric[] | undefined;
	export let selected: string;

	let showNewTag = false;
	let showUpdateTag = false;

	const zenoClient = getContext('zenoClient') as ZenoService;

	$: choices = $project.view === '' ? ['table'] : ['list', 'table'];
	$: selected = choices[0];

	function saveChanges() {
		if ($editTag === undefined) return;
		filterSelection.set(false);
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
{#if showUpdateTag}
	<UpdateTagPopup on:close={() => (showUpdateTag = false)} />
{/if}
<div class="w-full">
	<div class="mt-2 flex min-h-[50px] w-full justify-between">
		<ChipsWrapper />
	</div>
	{#if !$page.url.href.includes('compare') || $selectionIds.length > 0 || $editTag !== undefined}
		<div class="flex w-full flex-wrap items-center pb-2">
			<div class="mr-4 flex items-center">
				{#if !$page.url.href.includes('compare') && currentResult !== undefined && currentResult.length > 0}
					{#if currentResult[0].metric !== undefined && currentResult[0].metric !== null}
						<span class="mr-3 text-grey-dark">
							{$metric ? $metric.name + ':' : ''}
						</span>
						<span class="mr-3 text-primary">
							{currentResult[0].metric.toFixed(2)}
						</span>
					{/if}
					<span class="mr-2.5 italic text-grey-darker"
						>({currentResult[0].size.toLocaleString()} instance{currentResult[0].size > 1
							? 's'
							: ''})</span
					>
				{/if}
				{#if $project.editor && ($selectionIds.length > 0 || $editTag !== undefined)}
					<div class="flex items-center">
						<button
							class="mx-1 flex w-fit rounded-2xl border-2 bg-secondary-light {$filterSelection
								? 'border-secondary'
								: 'border-secondary-light'} px-2.5 py-1"
							on:click={() => filterSelection.set(!$filterSelection)}
						>
							<span
								>{$selectionIds.length} instance{$selectionIds.length > 1 ? 's' : ''} selected</span
							>
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
							class="!text-secondary"
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
						{#if $editTag === undefined && $tags.length > 0}
							<Button
								variant="outlined"
								class="ml-2 !text-secondary"
								on:keydown={() => ({})}
								on:click={() => {
									showUpdateTag = true;
								}}
							>
								Add to Tag
							</Button>
						{/if}
					</div>
				{/if}
			</div>
			{#if !$page.url.href.includes('compare')}
				<div class="ml-auto flex items-center">
					<Group>
						{#each choices as choice}
							<Button
								variant="outlined"
								class={selected === choice ? 'bg-grey-lighter' : 'bg-white'}
								on:click={() => (selected = choice)}>{choice}</Button
							>
						{/each}
					</Group>
				</div>
			{/if}
		</div>
	{/if}
</div>
