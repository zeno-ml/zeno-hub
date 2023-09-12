<script lang="ts">
	import { resolveDataPoint } from '$lib/util/util';
	import CircularProgress from '@smui/circular-progress';

	export let entry: Record<string, number | string | boolean>;
	export let modelColumn: string;
</script>

<div class="p-4 border border-grey-lighter max-w-[450px] min-w-[400px] rounded">
	{#await resolveDataPoint(entry)}
		<CircularProgress style="height: 32px; width: 32px; margin-right:20px" indeterminate />
	{:then audioResponse}
		{@const audioURL = audioResponse.toString()}
		<audio controls src={audioURL}>
			<source src={audioURL} type={'audio/' + audioURL.split('.').at(-1)} />
		</audio>
	{/await}
	<div />
	<p class="mt-3 text-grey">
		<span class="font-semibold">label: </span>
		{entry['label']}
	</p>
	{#if modelColumn && entry[modelColumn] !== undefined}
		<p class="mt-2 text-grey">
			<span class="font-semibold">output: </span>
			{entry[modelColumn]}
		</p>
	{/if}
</div>
