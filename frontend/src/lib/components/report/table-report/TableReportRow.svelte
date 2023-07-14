<script lang="ts">
	import { Cell, Row } from '@smui/data-table';
	import SliceDetailsContainer from './SliceDetailsContainer.svelte';
	import { slices } from '$lib/stores';
	import { SlicesOrModels, type TableParameters } from '$lib/zenoapi';

	export let columns: string[] | number[];
	export let tableRecord: Record<
		string | number,
		Record<string | number, { fixedValue: number; size: number }>
	>;
	export let parameters: TableParameters;
	export let row: string | number;
</script>

<Row style="overflow: visible">
	<!-- y cell -->
	<Cell>
		{#if parameters.yChannel === SlicesOrModels.SLICES}
			<SliceDetailsContainer sli={$slices.find((sli) => sli.id === row)} />
		{:else}
			{row}
		{/if}
	</Cell>
	{#each columns as column}
		<Cell style="text-align: center;">
			<p>
				{tableRecord[column][row].fixedValue.toFixed(2)}
			</p>
		</Cell>
	{/each}
</Row>

<style>
	:global(.sticky) {
		overflow: visible;
		left: 0px;
		background: var(--G6);
		z-index: 0;
	}
</style>
