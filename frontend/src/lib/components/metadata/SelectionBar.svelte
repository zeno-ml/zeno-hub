<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import { page } from '$app/stores';
	import { editTag, metric, project } from '$lib/stores';
	import type { GroupMetric } from '$lib/zenoapi';
	import { mdiRefresh } from '@mdi/js';
	import Button, { Group, Icon } from '@smui/button';
	import CircularProgress from '@smui/circular-progress';
	import { tooltip } from '@svelte-plugins/tooltips';
	import ChipsWrapper from './ChipsWrapper.svelte';

	export let currentResult: GroupMetric[] | undefined;
	export let selected = 'list';

	let CHOICES: string[];

	let runningAnalysis = true;

	$: CHOICES =
		$editTag === undefined
			? $project !== undefined && $project.view !== ''
				? ['list', 'table']
				: ['table']
			: ['table'];

	$: {
		if ($project === undefined) {
			runningAnalysis = true;
		} else {
			runningAnalysis = false;
		}
	}
</script>

<div style:width="100%">
	<div class="pt-2.5 flex justify-between w-full border-b border-grey-lighter">
		<ChipsWrapper />
		<div class="status flex items-center">
			{#if runningAnalysis}
				<CircularProgress
					class="status-circle"
					style="height: 32px; width: 32px; margin-right:20px"
					indeterminate
				/>
			{:else}
				<div
					on:keydown={() => ({})}
					on:click={() => invalidateAll()}
					use:tooltip={{
						content: 'Refresh data & functions',
						position: 'left',
						theme: 'zeno-tooltip'
					}}
				>
					<div class="cursor-pointer w-6 h-6 fill-grey">
						<Icon style="outline:none" tag="svg" viewBox="0 0 24 24">
							<path d={mdiRefresh} />
						</Icon>
					</div>
				</div>
			{/if}
		</div>
	</div>
	{#if !$page.url.href.includes('compare')}
		<div
			class="flex flex-wrap justify-between w-full items-center py-2.5 border-b border-grey-lighter"
		>
			<div>
				{#if currentResult}
					{#if currentResult[0].metric !== undefined && currentResult[0].metric !== null}
						<span class="text-grey-dark mr-3">
							{$metric ? $metric.name + ':' : ''}
						</span>
						<span class="text-primary mr-3">
							{currentResult[0].metric.toFixed(2)}
						</span>
					{/if}
					<span class="italic text-grey-darker mr-2.5"
						>({currentResult[0].size.toLocaleString()} instances)</span
					>
				{/if}
			</div>
			<div class="flex items-center">
				{#if $editTag === undefined}
					<slot />
					<Group>
						{#if $project !== undefined}
							{#each CHOICES as choice}
								<Button
									style="background-color: {selected === choice ? 'var(--G5)' : 'var(--G6)'}"
									variant="outlined"
									on:click={() => (selected = choice)}>{choice}</Button
								>
							{/each}
						{/if}
					</Group>
				{:else}
					<div class="flex items-center" style="margin-right: 10px">
						<p style="margin: auto; margin-right: 10px">Editing</p>
						<div class="py-1 px-2.5 bg-greenish-light mx-1 my rounded width-fit margin-auto">
							{$editTag.tagName}
						</div>
					</div>
				{/if}
			</div>
		</div>
	{/if}
</div>
