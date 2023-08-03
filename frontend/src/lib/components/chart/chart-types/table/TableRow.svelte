<script lang="ts">
	import { slices } from '$lib/stores';
	import { SlicesOrModels, type TableParameters } from '$lib/zenoapi';
	import { Cell, Row } from '@smui/data-table';
	import SliceDetailsContainer from './SliceDetailsContainer.svelte';

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
		{#if tableRecord[column] !== undefined && tableRecord[column][row] !== undefined}
			<Cell style="text-align: center;">
				<p>
					{tableRecord[column][row].fixedValue.toFixed(2)}
				</p>
			</Cell>
		{/if}
	{/each}
</Row>
