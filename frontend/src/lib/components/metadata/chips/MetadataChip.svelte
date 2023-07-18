<script lang="ts">
	import { selections } from '$lib/stores';
	import { Join, MetadataType, type FilterPredicate } from '$lib/zenoapi';
	import { TrailingIcon } from '@smui/chips';

	export let chip: FilterPredicate[];
	export let hash: string;
</script>

<div class="meta-chip">
	<span>
		{#if chip[0].column.dataType === MetadataType.CONTINUOUS}
			{parseFloat(`${chip[0].value}`).toFixed(2)}
			{'<='}
			{chip[0].column.name}
			{'<='}
			{parseFloat(`${chip[1].value}`).toFixed(2)}
		{:else if chip[0].column.dataType === MetadataType.BOOLEAN}
			{chip[0].value}
			{chip[0].column.name}
		{:else if chip[0].column.dataType === MetadataType.NOMINAL}
			{chip[0].column.name} {'=='} {" '" + chip[0].value + "'"}
		{:else}
			{chip[0].column.name}
			{'=='}
			{chip.map((c) => c.value).join(' | ')}
		{/if}
	</span>
	<TrailingIcon
		class="remove material-icons"
		on:click={() =>
			selections.update((m) => ({
				slices: m.slices,
				metadata: {
					...m.metadata,
					[hash]: { predicates: [], join: Join.AND }
				},
				tags: m.tags
			}))}
	>
		cancel
	</TrailingIcon>
</div>

<style>
	.meta-chip {
		padding: 5px 10px;
		background: var(--P3);
		margin-left: 5px;
		margin-right: 5px;
		margin-top: 2px;
		margin-bottom: 2px;
		border-radius: 4px;
		width: fit-content;
	}
</style>
