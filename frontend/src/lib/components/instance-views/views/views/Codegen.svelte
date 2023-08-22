<script lang="ts">
	import { HighlightAuto } from 'svelte-highlight';
	import 'svelte-highlight/styles/github.css';

	// Objects with keys corresponding to the following props.
	export let entry: Record<string, string | number | boolean>;
	// Key for model outputs.
	export let modelColumn: string;
</script>

<div id="w-min p-2 border border-grey-lighter">
	{#if entry['data_id']}
		<HighlightAuto code={entry['data_id']} />
	{/if}
	{#if entry['label']}
		<hr />
		<pre class="mt-2 mb-0">label</pre>
		<HighlightAuto code={entry['label']} />
	{/if}
	{#if entry[modelColumn]}
		<hr />
		<pre class="mt-2 mb-0">model prediction</pre>
		<HighlightAuto code={entry[modelColumn]} />
	{/if}
</div>
