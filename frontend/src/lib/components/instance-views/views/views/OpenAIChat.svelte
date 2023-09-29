<script lang="ts">
	import { resolveDataPoint } from '$lib/util/util';
	import { mdiChevronUp } from '@mdi/js';
	import CircularProgress from '@smui/circular-progress/src/CircularProgress.svelte';
	import AssistantBlock from './openai-chat/AssistantBlock.svelte';
	import SystemBlock from './openai-chat/SystemBlock.svelte';
	import UserBlock from './openai-chat/UserBlock.svelte';

	export let entry: Record<string, number | string | boolean | { role: string; content: string }[]>;
	export let modelColumn: string;

	$: showall = false;
	$: fetchJSON = (async () => {
		const response = await resolveDataPoint(entry);
		const resp = await (response as Response).json();
		showall = resp.length <= 5;
		return resp;
	})();

	function entryString(
		value: number | string | boolean | { role: string; content: string }[]
	): string {
		return `${value}`;
	}
</script>

{#await fetchJSON}
	<CircularProgress style="height: 32px; width: 32px; margin-right:20px" indeterminate />
{:then data}
	{@const entries = showall ? data : data.slice(-4)}
	<div class="flex flex-col border border-grey-light rounded p-2.5 m-1 w-[32rem]">
		{#if !showall}
			<button
				class="self-center bg-transparent cursor-pointer flex items-center p-1 -mt-1.5 rounded-2xl hover:bg-grey-lighter"
				on:click={() => (showall = true)}
			>
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="w-6 fill-grey-darker">
					<path d={mdiChevronUp} />
				</svg>
				<span class="pr-1">Show All</span>
			</button>
		{/if}
		{#if data}
			{#each entries as item}
				{#if item['role'] === 'system'}
					<SystemBlock input={item['content']} />
				{:else if item['role'] === 'assistant'}
					<AssistantBlock input={item['content']} />
				{:else if item['role'] === 'user'}
					<UserBlock input={item['content']} />
				{/if}
			{/each}
		{/if}
		{#if entry[modelColumn]}
			<AssistantBlock input={entryString(entry[modelColumn])} output={true} />
		{/if}
		{#if entry['label']}
			<div class="flex flex-col -mx-2.5 -mb-2.5 mt-2.5 p-1 border-t border-grey-lighter">
				<span class="font-medium">Expected:</span>
				<span>{entry['label']}</span>
			</div>
		{/if}
	</div>
{/await}
