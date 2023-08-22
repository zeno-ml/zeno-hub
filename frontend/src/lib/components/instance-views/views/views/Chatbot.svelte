<script lang="ts">
	import { resolveDataPoint } from '$lib/util/util';
	import CircularProgress from '@smui/circular-progress/src/CircularProgress.svelte';
	import AssistantBlock from './chatbot/AssistantBlock.svelte';
	import UserBlock from './chatbot/UserBlock.svelte';

	export let entry: Record<string, number | string | boolean>;
	export let modelColumn: string;

	$: fetchJSON = (async () => {
		const response = await resolveDataPoint(entry);
		const resp = await (response as Response).json();
		return resp;
	})();
	$: modelContent = entry[modelColumn] as string;
</script>

{#await fetchJSON}
	<CircularProgress style="height: 32px; width: 32px; margin-right:20px" indeterminate />
{:then data}
	<div id="border border-grey-lighter rounded p-2.5">
		<UserBlock input={data} />
		{#if entry[modelColumn]}
			<AssistantBlock input={modelContent} output={true} />
		{/if}
		{#if entry['label']}
			<p class="m-2"><span class="mr-1 font-bold">expected:</span> {entry['label']}</p>
		{/if}
	</div>
{/await}
