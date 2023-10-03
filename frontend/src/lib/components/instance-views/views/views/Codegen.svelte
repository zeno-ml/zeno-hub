<script lang="ts">
	import { resolveDataPoint } from '$lib/util/util';
	import CircularProgress from '@smui/circular-progress/src/CircularProgress.svelte';
	import { HighlightAuto } from 'svelte-highlight';
	import 'svelte-highlight/styles/github.css';

	// Objects with keys corresponding to the following props.
	export let entry: Record<string, string | number | boolean>;
	// Key for model outputs.
	export let modelColumn: string;
	export let dataColumn: string;
	export let labelColumn: string;
</script>

<div id="w-min p-2 border border-grey-lighter">
	{#await resolveDataPoint(entry[dataColumn])}
		<CircularProgress style="height: 32px; width: 32px; margin-right:20px" indeterminate />
	{:then textData}
		<HighlightAuto code={textData} />
	{/await}
	{#if entry[labelColumn]}
		<hr />
		<pre class="mt-2 mb-0">label</pre>
		<HighlightAuto code={entry[labelColumn]} />
	{/if}
	{#if entry[modelColumn]}
		<hr />
		<pre class="mt-2 mb-0">prediction</pre>
		<HighlightAuto code={entry[modelColumn]} />
	{/if}
</div>
