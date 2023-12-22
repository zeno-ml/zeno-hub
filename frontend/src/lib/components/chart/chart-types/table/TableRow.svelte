<script lang="ts">
	import { SlicesOrModels, type Slice, type TableParameters } from '$lib/zenoapi';
	import { Cell, Row } from '@smui/data-table';
	import SliceDetailsContainer from './SliceDetailsContainer.svelte';

	export let columns: (string | number)[];
	export let tableRecord: Record<
		string | number,
		Record<string | number, { fixedValue: number; size: number }>
	>;
	export let parameters: TableParameters;
	export let row: string | number;
	export let slices: Slice[];
</script>

<Row class="overflow-visible">
	<!-- y cell -->
	<Cell>
		{#if parameters.yChannel === SlicesOrModels.SLICES}
			{#if row === -1}
				<p>All instances</p>
			{:else}
				<SliceDetailsContainer sli={slices.find((sli) => sli.id === row)} />
			{/if}
		{:else}
			{row}
		{/if}
	</Cell>
	{#each columns as column}
		{#if tableRecord[column] !== undefined && tableRecord[column][row] !== undefined}
			<Cell>
				{tableRecord[column][row].fixedValue.toLocaleString()}
			</Cell>
		{/if}
	{/each}
</Row>
