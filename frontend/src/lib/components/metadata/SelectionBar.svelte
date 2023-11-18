<script lang="ts">
	import { page } from '$app/stores';
	import { metric, project } from '$lib/stores';
	import type { GroupMetric } from '$lib/zenoapi';
	import Button, { Group } from '@smui/button';
	import ChipsWrapper from './ChipsWrapper.svelte';

	export let currentResult: GroupMetric[] | undefined;
	export let selected: string;

	$: choices = $project.view === '' ? ['table'] : ['list', 'table'];
	$: selected = choices[0];
</script>

<div class="w-full">
	<div class="flex min-h-[60px] w-full justify-between border-b border-grey-lighter pt-2.5">
		<ChipsWrapper />
	</div>
	{#if !$page.url.href.includes('compare')}
		<div class="flex w-full flex-wrap items-center border-b border-grey-lighter py-2.5">
			<div class="mr-4 flex">
				{#if currentResult !== undefined && currentResult.length > 0}
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
			</div>
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
		</div>
	{/if}
</div>
