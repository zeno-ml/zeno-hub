<script lang="ts">
	import { page } from '$app/stores';
	import { editTag, metric, project } from '$lib/stores';
	import type { GroupMetric } from '$lib/zenoapi';
	import Button, { Group } from '@smui/button';
	import ChipsWrapper from './ChipsWrapper.svelte';

	export let currentResult: Promise<GroupMetric[] | undefined>;
	export let selected: string;

	$: choices =
		$editTag !== undefined || $project.view === '' ? ['table'] : ['list', 'table', 'scatter'];
	$: selected = choices[0];
</script>

<div class="w-full">
	<div class="flex h-[60px] w-full justify-between border-b border-grey-lighter pt-2.5">
		<ChipsWrapper />
	</div>
	{#if !$page.url.href.includes('compare')}
		<div
			class="flex w-full flex-wrap items-center justify-between border-b border-grey-lighter py-2.5"
		>
			<div class="flex">
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
							>({res[0].size.toLocaleString()} instances)</span
						>
					{/if}
				{/await}
			</div>
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
