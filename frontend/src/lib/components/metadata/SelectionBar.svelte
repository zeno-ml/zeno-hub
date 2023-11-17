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
	import ChipsWrapper from './ChipsWrapper.svelte';

	export let currentResult: Promise<GroupMetric[] | undefined> | undefined;
	export let selected: string;

	let showNewTag = false;

	const zenoClient = getContext('zenoClient') as ZenoService;

	$: choices = $project.view === '' ? ['table'] : ['list', 'table'];
	$: selected = choices[0];

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
<div class="w-full">
	<div class="flex h-[60px] w-full justify-between border-b border-grey-lighter pt-2.5">
		<ChipsWrapper />
	</div>
	{#if !$page.url.href.includes('compare') || $selectionIds.length > 0 || $editTag}
		<div class="flex w-full flex-wrap items-center border-b border-grey-lighter py-2.5">
			{#if !$page.url.href.includes('compare')}
				<div class="mr-4 flex">
					{#await currentResult then res}
						{#if res !== undefined && res.length > 0}
							{#if res[0].metric !== undefined && res[0].metric !== null}
								<span class="mr-3 text-grey-dark">
									{$metric ? $metric.name + ':' : ''}
								</span>
								<span class="mr-3 text-primary">
									{res[0].metric.toFixed(2)}
								</span>
							{/if}
							<span class="mr-2.5 italic text-grey-darker"
								>({res[0].size.toLocaleString()} instance{res[0].size > 1 ? 's' : ''})</span
							>
						{/if}
					{/await}
				</div>
			{/if}
			{#if $selectionIds.length > 0}
				<div class="flex items-center">
					<button
						class="my flex w-fit rounded-lg border-2 {$filterSelection
							? 'bg-greenish-light'
							: ''} border-greenish-light px-2.5 py-1"
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
							}}>cancel</TrailingIcon
						>
					</button>
					<Button
						variant="outlined"
						class="ml-2"
						style="background-color: var(--N1); color: white; "
						on:keydown={() => ({})}
						on:click={() => {
							if ($editTag === undefined) showNewTag = true;
							else {
								saveChanges();
							}
						}}
					>
						{$editTag === undefined ? 'Create Tag' : 'Done'}
					</Button>
				</div>
			{/if}
			{#if !$page.url.href.includes('compare')}
				<div class="ml-auto flex items-center">
					<slot />
					<Group>
						{#each choices as choice}
							<Button
								style="background-color: {selected === choice ? 'var(--G5)' : 'var(--G6)'}"
								variant="outlined"
								on:click={() => (selected = choice)}>{choice}</Button
							>
						{/each}
					</Group>
				</div>
			{/if}
		</div>
	{/if}
</div>
