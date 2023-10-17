<script lang="ts">
	import Markdown from '$lib/components/general/Markdown.svelte';
	import { mdiChevronDown, mdiChevronUp } from '@mdi/js';
	import purify from 'isomorphic-dompurify';
	import { parse } from 'marked';
	import AssistantBlock from './openai-chat-markdown/AssistantBlock.svelte';
	import SystemBlock from './openai-chat-markdown/SystemBlock.svelte';
	import UserBlock from './openai-chat-markdown/UserBlock.svelte';

	export let entry: Record<string, number | string | boolean | { role: string; content: string }[]>;
	export let modelColumn: string;
	export let dataColumn: string;
	export let labelColumn: string;

	const data = JSON.parse(entry[dataColumn] as string).map((e: any) => {
		e['output'] = false;
		return e;
	});
	let renderedLabel = '';
	let outputData: { role: string; content: string; output: boolean }[] = [];

	if (modelColumn) {
		try {
			outputData = JSON.parse(entry[modelColumn] as string).map((e: any) => {
				e['output'] = true;
				return e;
			});
		} catch {
			outputData = [{ role: 'assistant', content: entry[modelColumn] as string, output: true }];
		}
	}

	let allData = [...data, ...outputData];
	let showAll = allData.length <= 5;

	$: if (entry[labelColumn]) {
		renderedLabel = purify.sanitize(parse(entry[labelColumn] as string));
	}

	$: shownData = showAll ? allData : allData.slice(-4);
</script>

<div class="flex flex-col border border-grey-light rounded p-2.5 m-1 max-w-4xl">
	{#if allData.length > 4}
		<button
			class="self-center bg-transparent cursor-pointer flex items-center p-1 -mt-1.5 rounded-2xl hover:bg-grey-lighter"
			on:click={() => (showAll = !showAll)}
		>
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="w-6 fill-grey-darker">
				<path d={showAll ? mdiChevronDown : mdiChevronUp} />
			</svg>
			<span class="pr-1">Show {showAll ? 'Less' : 'All'}</span>
		</button>
	{/if}
	{#if shownData}
		{#key shownData}
			{#each shownData as item}
				{#if item['role'] === 'system'}
					<SystemBlock input={item['content']} />
				{:else if item['role'] === 'assistant'}
					<AssistantBlock input={item['content']} output={item['output']} />
				{:else if item['role'] === 'user'}
					<UserBlock input={item['content']} output={item['output']} />
				{/if}
			{/each}
		{/key}
	{/if}
	{#if entry[labelColumn]}
		<div class="flex flex-col -mx-2.5 -mb-2.5 mt-2.5 p-1 border-t border-grey-lighter">
			<span class="font-medium">Expected:</span>
			<span>
				<Markdown renderedText={renderedLabel} />
			</span>
		</div>
	{/if}
</div>
