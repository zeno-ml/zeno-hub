<script lang="ts">
	import AssistantBlock from './chatbot/AssistantBlock.svelte';
	import UserBlock from './chatbot/UserBlock.svelte';

	export let entry: Record<string, number | string | boolean>;
	export let modelColumn: string;

	$: chatData = entry['data'] as string;
	$: modelContent = entry[modelColumn] as string;
</script>

<div id="container">
	<UserBlock input={chatData} />
	{#if entry[modelColumn]}
		<AssistantBlock input={modelContent} output={true} />
	{/if}
	{#if entry['label']}
		<p><span class="label">expected:</span> {entry['label']}</p>
	{/if}
</div>

<style>
	#container {
		border: 0.5px solid rgb(224, 224, 224);
		min-width: 350px;
		border-radius: 2px;
		padding: 10px;
	}
	.label {
		margin-right: 5px;
		font-weight: 700;
	}
	p {
		margin: 5px;
		overflow-wrap: anywhere;
	}
</style>
