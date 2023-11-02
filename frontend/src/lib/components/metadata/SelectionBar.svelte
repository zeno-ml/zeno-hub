<script lang="ts">
	import { page } from '$app/stores';
	import { editTag, metric, project, selectionIds } from '$lib/stores';
	import type { GroupMetric } from '$lib/zenoapi';
	import Button, { Group } from '@smui/button';
	import { TrailingIcon } from '@smui/chips';
	import TagPopup from '../popups/TagPopup.svelte';
	import ChipsWrapper from './ChipsWrapper.svelte';

	export let currentResult: Promise<GroupMetric[] | undefined>;
	export let selected: string;

	let showNewTag = false;

	$: choices = $editTag !== undefined || $project.view === '' ? ['table'] : ['list', 'table'];
	$: selected = choices[0];
</script>

{#if showNewTag}
	<TagPopup on:close={() => (showNewTag = false)} />
{/if}
<div class="w-full">
	<div class="flex h-[60px] w-full justify-between border-b border-grey-lighter pt-2.5">
		<ChipsWrapper />
	</div>
	{#if !$page.url.href.includes('compare')}
		<div class="flex w-full flex-wrap items-center border-b border-grey-lighter py-2.5">
			<div class="mr-auto flex">
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
			{#if $selectionIds.length > 0}
				<button
					class="my mx-1 mr-4 flex w-fit rounded-lg border-2 border-greenish-light px-2.5 py-1"
					on:click={() => (showNewTag = true)}
				>
					<span>{$selectionIds.length} instance{$selectionIds.length > 1 ? 's' : ''} selected</span>
					<TrailingIcon class="remove material-icons" on:click={() => selectionIds.set([])}
						>cancel</TrailingIcon
					>
				</button>
			{/if}
			<div class="flex items-center">
				{#if $editTag === undefined}
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
				{:else}
					<div class="flex items-center" style="margin-right: 10px">
						<p style="margin: auto; margin-right: 10px">Editing</p>
						<div class="my width-fit margin-auto mx-1 rounded bg-greenish-light px-2.5 py-1">
							{$editTag.tagName}
						</div>
					</div>
				{/if}
			</div>
		</div>
	{/if}
</div>
