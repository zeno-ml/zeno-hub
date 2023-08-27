<script lang="ts">
	export let entry: Record<string, number | string | boolean>;
	export let modelColumn: string;

	$: audioURL = entry['data_id'] as string;
</script>

<div id="flex flex-wrap">
	<div class="p-2.5 border border-grey-lighter">
		<div style:display="flex">
			<audio controls src={audioURL}>
				<source src={audioURL} type={'audio/' + audioURL.split('.').at(-1)} />
			</audio>
		</div>
		<span class="text-xs">label: </span><span class="value">
			{entry['label']}
		</span>
		{#if modelColumn && entry[modelColumn] !== undefined}
			<br />
			<span class="text-xs">output: </span>
			<span class="text-xs">{entry[modelColumn]} </span>
		{/if}
	</div>
</div>
