<script lang="ts">
	import { page } from '$app/stores';
	import { editTag, metric, project } from '$lib/stores';
	import type { GroupMetric } from '$lib/zenoapi';
	import Button, { Group } from '@smui/button';
	import ChipsWrapper from './ChipsWrapper.svelte';

	export let currentResult: Promise<GroupMetric[] | undefined>;
	export let selected = 'list';

	let CHOICES: string[];

	$: CHOICES =
		$editTag === undefined
			? $project !== undefined && $project.view !== ''
				? ['list', 'table']
				: ['table']
			: ['table'];
</script>

<div class="w-full">
	<div class="pt-2.5 flex justify-between w-full border-b border-grey-lighter h-[60px]">
		<ChipsWrapper />
	</div>
	{#if !$page.url.href.includes('compare')}
		<div
			class="flex flex-wrap justify-between w-full items-center py-2.5 border-b border-grey-lighter"
		>
			<div class="flex">
				<span class="text-grey-dark mr-3">
					{$metric ? $metric.name + ':' : ''}
				</span>
				{#await currentResult then res}
					{#if res !== undefined && res.length > 0}
						{#if res[0].metric !== undefined && res[0].metric !== null}
							<span class="text-primary mr-3">
								{res[0].metric.toFixed(2)}
							</span>
						{/if}
						<span class="italic text-grey-darker mr-2.5"
							>({res[0].size.toLocaleString()} instances)</span
						>
					{/if}
				{/await}
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
