<script lang="ts">
	import Markdown from '$lib/components/general/Markdown.svelte';
	import { mdiChevronUp } from '@mdi/js';
	import purify from 'isomorphic-dompurify';
	import { parse } from 'marked';
	import AssistantBlock from './openai-chat-markdown/AssistantBlock.svelte';
	import SystemBlock from './openai-chat-markdown/SystemBlock.svelte';
	import UserBlock from './openai-chat-markdown/UserBlock.svelte';

	export let entry: Record<string, number | string | boolean | { role: string; content: string }[]>;
	export let modelColumn: string;
	export let dataColumn: string;
	export let labelColumn: string;

	let renderedLabel = '';
	const data = JSON.parse(entry[dataColumn] as string);
	let showAll = data.length <= 5;

	$: shownData = showAll ? data : data.slice(-4);

	$: if (entry[labelColumn]) {
		renderedLabel = purify.sanitize(parse(entry[labelColumn] as string));
	}

	function entryString(
		value: number | string | boolean | { role: string; content: string }[]
	): string {
		return `${value}`;
	}
</script>

<div class="flex flex-col border border-grey-light rounded p-2.5 m-1 max-w-4xl">
	{#if !showAll}
		<button
			class="self-center bg-transparent cursor-pointer flex items-center p-1 -mt-1.5 rounded-2xl hover:bg-grey-lighter"
			on:click={() => (showAll = true)}
		>
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="w-6 fill-grey-darker">
				<path d={mdiChevronUp} />
			</svg>
			<span class="pr-1">Show All</span>
		</button>
	{/if}
	{#if shownData}
		{#key shownData}
			{#each shownData as item}
				{#if item['role'] === 'system'}
					<SystemBlock input={item['content']} />
				{:else if item['role'] === 'assistant'}
					<AssistantBlock input={item['content']} />
				{:else if item['role'] === 'user'}
					<UserBlock input={item['content']} />
				{/if}
			{/each}
		{/key}
	{/if}
	{#if entry[modelColumn]}
		<AssistantBlock input={entryString(entry[modelColumn])} output={true} />
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
