<script lang="ts">
	import { noop } from 'svelte/internal';
	import AssistantBlock from './openai-chat/AssistantBlock.svelte';
	import SystemBlock from './openai-chat/SystemBlock.svelte';
	import UserBlock from './openai-chat/UserBlock.svelte';

	export let entry: Record<string, number | string | boolean | { role: string; content: string }[]>;
	export let modelColumn: string;

	let hovered = false;

	$: chatData = entry['data'] as { role: string; content: string }[];
	$: showall = chatData.length <= 5;
	$: entries = showall ? chatData : chatData.slice(-4);
</script>

<div id="container">
	{#if !showall}
		<div
			class="show-all"
			class:hover={hovered}
			on:click={() => (showall = true)}
			on:keydown={noop}
			on:focus={() => (hovered = true)}
			on:blur={() => (hovered = false)}
			on:mouseover={() => (hovered = true)}
			on:mouseout={() => (hovered = false)}
		>
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
				<path d="m12 8-6 6 1.41 1.41L12 10.83l4.59 4.58L18 14z" />
			</svg>
			<span>Show All</span>
		</div>
	{/if}
	{#if chatData}
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
		<AssistantBlock input={entry[modelColumn]} output={true} />
	{/if}
	{#if entry['label']}
		<div class="expected">
			<span class="label">Expected:</span>
			<span>{entry['label']}</span>
		</div>
	{/if}
</div>

<style>
	#container {
		display: flex;
		flex-direction: column;
		border: 1px solid rgb(224, 224, 224);
		min-width: 350px;
		max-width: 550px;
		border-radius: 2px;
		padding: 10px;
		margin: 2.5px;
	}
	.label {
		font-weight: 500;
	}
	.show-all {
		align-self: center;
		border: none;
		background-color: transparent;
		cursor: pointer;
		display: flex;
		align-items: center;
		padding: 5px;
		margin-top: -7px;
		border-radius: 20px;
	}
	.hover {
		background-color: var(--G5);
	}
	.show-all span {
		padding-right: 5px;
	}
	.show-all svg {
		min-width: 24px;
		width: 24px;
		fill: var(--G3);
	}
	.expected {
		overflow-wrap: break-word;
		display: flex;
		flex-direction: column;
		margin-left: -10px;
		margin-bottom: -10px;
		margin-right: -10px;
		padding: 5px;
		font-size: small;
		margin-top: 10px;
		border-top: 0.5px solid rgb(224, 224, 224);
	}
</style>
