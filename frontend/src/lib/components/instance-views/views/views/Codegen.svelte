<script lang="ts">
	import { HighlightAuto } from 'svelte-highlight';
	import 'svelte-highlight/styles/github.css';

	// Objects with keys corresponding to the following props.
	export let entry: Record<string, string | number | boolean>;
	// Key for model outputs.
	export let modelColumn: string;
</script>

<div id="container">
	{#if entry['item']}
		<HighlightAuto code={entry['item']} />
	{/if}
	{#if entry['label']}
		<hr />
		<pre class="label">label</pre>
		<HighlightAuto code={entry['label']} />
	{/if}
	{#if entry[modelColumn]}
		<hr />
		<pre class="label">model prediction</pre>
		<HighlightAuto code={entry[modelColumn]} />
	{/if}
</div>

<style>
	#container {
		width: min-content;
		padding: 5px;
		border: 0.5px solid rgb(224, 224, 224);
	}
	.label {
		margin-top: 5px;
		margin-bottom: 0px;
	}
	:global(pre code.hljs) {
		background: var(--Y2);
	}
</style>
