<script lang="ts">
	export let entry: Record<string, number | string | boolean>;
	export let modelColumn: string;
	export let dataColumn: string;
	export let labelColumn: string;
</script>

<div class="p-4 border border-grey-lighter max-w-[350px] min-w-[350px] rounded">
	<audio controls src={`${entry[dataColumn]}`}>
		<source
			src={`${entry[dataColumn]}`}
			type={'audio/' + `${entry[dataColumn]}`.split('.').at(-1)}
		/>
	</audio>
	<div />
	<p class="mt-3 text-grey">
		<span class="font-semibold">label: </span>
		{entry[labelColumn]}
	</p>
	{#if modelColumn && entry[modelColumn] !== undefined}
		<p class="mt-2 text-grey">
			<span class="font-semibold">output: </span>
			{entry[modelColumn]}
		</p>
	{/if}
</div>
