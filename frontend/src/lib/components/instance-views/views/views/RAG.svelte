<script lang="ts">
	import { resolveDataPoint } from '$lib/util/util';
	import { mdiChevronDown, mdiChevronUp } from '@mdi/js';
	import CircularProgress from '@smui/circular-progress/';
	import RetrievedBlock from './rag/RetrievedBlock.svelte';

	export let entry: Record<string, number | string | boolean>;
	export let modelColumn: string;
	export let dataColumn: string;
	export let labelColumn: string;

	const data = JSON.parse(entry[modelColumn] as string);
	let showAll = data.length <= 5;

	$: shownDocs = showAll
		? data['retrieved'].sort(
				(
					a: { reference: string; text: string; score: string },
					b: { reference: string; text: string; score: string }
				) => a.score < b.score
		  )
		: data['retrieved']
				.sort(
					(
						a: { reference: string; text: string; score: string },
						b: { reference: string; text: string; score: string }
					) => a.score < b.score
				)
				.slice(0, 5);
</script>

<div class="flex flex-col border border-grey-light rounded p-2.5 m-1 w-[32rem]">
	{#await resolveDataPoint(entry[dataColumn])}
		<CircularProgress style="height: 32px; width: 32px; margin-right:20px" indeterminate />
	{:then textData}
		<p class="text-grey whitespace-pre-wrap">
			<span class="font-semibold">input: </span>
			{textData}
		</p>
	{/await}
	{#if entry[labelColumn] !== undefined}
		{#await resolveDataPoint(entry[labelColumn])}
			<CircularProgress style="height: 32px; width: 32px; margin-right:20px" indeterminate />
		{:then textData}
			<p class="text-grey whitespace-pre-wrap">
				<span class="font-semibold">label: </span>
				{textData}
			</p>
		{/await}
	{/if}
	{#if modelColumn && entry[modelColumn] !== undefined}
		<hr class="mt-2 mb-2 text-grey-darker" />
		{#if data['answer']}
			<p class="text-grey whitespace-pre-wrap">
				<span class="font-semibold">answer: </span>
				{data['answer']}
			</p>
		{/if}
		<span class="font-semibold">documents: </span>
		{#if shownDocs}
			{#key shownDocs}
				{#each shownDocs as item}
					<RetrievedBlock document={item} />
				{/each}
			{/key}
		{/if}
		<button
			class="self-center bg-transparent cursor-pointer flex items-center p-1 rounded-2xl hover:bg-grey-lighter"
			on:click={() => (showAll = !showAll)}
		>
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="w-6 fill-grey-darker">
				<path d={showAll ? mdiChevronDown : mdiChevronUp} />
			</svg>
			<span class="pr-1">Show {showAll ? 'Less' : 'All'}</span>
		</button>
	{/if}
</div>
