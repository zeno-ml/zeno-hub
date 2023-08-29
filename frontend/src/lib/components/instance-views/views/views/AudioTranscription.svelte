<script lang="ts">
	export let entry: Record<string, number | string | boolean>;
	export let modelColumn: string;

	$: audioURL = entry['data_id'] as string;
</script>

<div class="p-4 border border-grey-lighter max-w-[450px] min-w-[400px] rounded">
	<div>
		<audio controls src={audioURL}>
			<source src={audioURL} type={'audio/' + audioURL.split('.').at(-1)} />
		</audio>
	</div>
	<p class="mt-3 text-grey">
		<span class="font-semibold">label: </span>
		<span class="value">
			{entry['label']}
		</span>
	</p>
	{#if modelColumn && entry[modelColumn] !== undefined}
		<p class="mt-2 text-grey">
			<span class="font-semibold">output: </span>
			<span>{entry[modelColumn]} </span>
		</p>
	{/if}
</div>
