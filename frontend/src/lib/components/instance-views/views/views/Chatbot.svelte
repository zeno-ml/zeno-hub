<script lang="ts">
	import AssistantBlock from './chatbot/AssistantBlock.svelte';
	import UserBlock from './chatbot/UserBlock.svelte';

	export let entry: Record<string, number | string | boolean>;
	export let modelColumn: string;

	$: chatData = entry['data'] as string;
	$: modelContent = entry[modelColumn] as string;
</script>

<div id="border border-grey-lighter rounded p-2.5">
	<UserBlock input={chatData} />
	{#if entry[modelColumn]}
		<AssistantBlock input={modelContent} output={true} />
	{/if}
	{#if entry['label']}
		<p class="m-2"><span class="mr-1 font-bold">expected:</span> {entry['label']}</p>
	{/if}
</div>
