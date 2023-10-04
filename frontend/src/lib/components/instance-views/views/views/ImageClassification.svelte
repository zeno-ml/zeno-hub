<script lang="ts">
	export let entry: Record<string, number | string | boolean>;
	export let modelColumn: string;
	export let dataColumn: string;
	export let labelColumn: string;
</script>

<div class="w-min p-2 border border-grey-lighter" style:background-color="white">
	<img
		src={`${entry[dataColumn]}`}
		style:max-width="200px"
		alt="Image thumbnail for instance {entry[dataColumn]}"
	/>
	<br />
	<div class="flex">
		<span class="mr-2 text-xs">label: </span>
		<span class="value text-xs">{entry[labelColumn]}</span>
	</div>
	{#if modelColumn && entry[modelColumn]}
		<div class="flex">
			<span class="mr-2 text-xs">output: </span>
			<span class="value text-xs">{entry[modelColumn]} </span>
		</div>
	{/if}
</div>
