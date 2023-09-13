<script lang="ts">
	import { metrics, slices } from '$lib/stores';
	import {
		SlicesMetricsOrModels,
		SlicesOrModels,
		type Chart,
		type TableParameters
	} from '$lib/zenoapi';
	import { Icon } from '@smui/button';
	import DataTable, { Body, Cell, Head, Row } from '@smui/data-table';
	import SliceDetailsContainer from './SliceDetailsContainer.svelte';
	import TableRow from './TableRow.svelte';

	export let chart: Chart;
	export let data: {
		table: Array<{
			x_value: string | number;
			y_value: string | number;
			fixed_value: number;
			size: number;
		}>;
	};

	let tableRecord: Record<
		string | number,
		Record<string | number, { fixedValue: number; size: number }>
	> = {};

	let sortCol: { column: string | number | undefined; ascending: boolean } = {
		column: undefined,
		ascending: true
	};

	$: parameters = chart.parameters as TableParameters;
	$: columns =
		parameters.xChannel === SlicesMetricsOrModels.SLICES
			? parameters.slices
			: parameters.xChannel === SlicesMetricsOrModels.METRICS
			? parameters.metrics
			: parameters.models;
	$: rows = parameters.yChannel === SlicesOrModels.SLICES ? parameters.slices : parameters.models;
	$: {
		data, (tableRecord = {});
		data.table.map((cell) => {
			tableRecord[cell.x_value] === undefined
				? (tableRecord[cell.x_value] = {
						[cell.y_value]: { fixedValue: cell.fixed_value, size: cell.size }
				  })
				: (tableRecord[cell.x_value] = {
						...tableRecord[cell.x_value],
						[cell.y_value]: { fixedValue: cell.fixed_value, size: cell.size }
				  });
		});
	}
	$: {
		if (sortCol.column !== undefined) {
			if (sortCol.ascending) {
				rows = rows.sort(
					(rowA, rowB) =>
						tableRecord[sortCol.column ?? columns[0]][rowA].fixedValue -
						tableRecord[sortCol.column ?? columns[0]][rowB].fixedValue
				);
			} else {
				rows = rows.sort(
					(rowA, rowB) =>
						tableRecord[sortCol.column ?? columns[0]][rowB].fixedValue -
						tableRecord[sortCol.column ?? columns[0]][rowA].fixedValue
				);
			}
		}
	}
</script>

<div class="my-2">
	<DataTable>
		<Head>
			<Row>
				<Cell
					>{parameters.yChannel === SlicesOrModels.SLICES ? 'slices' : 'models'} \ {parameters.xChannel ===
					SlicesMetricsOrModels.SLICES
						? 'slices'
						: parameters.xChannel === SlicesMetricsOrModels.MODELS
						? 'models'
						: 'metrics'}</Cell
				>
				{#each columns as column}
					<Cell
						style="width: 140px; max-width: 140px; cursor: pointer;"
						on:keydown={() => ({})}
						on:click={() => {
							if (sortCol.column !== column) {
								sortCol = { column: column, ascending: true };
							} else {
								sortCol = { ...sortCol, ascending: !sortCol.ascending };
							}
						}}
					>
						<div style="display: flex;">
							<div style="margin:auto;overflow: hidden">
								{#if parameters.xChannel === SlicesMetricsOrModels.SLICES}
									<SliceDetailsContainer sli={$slices.find((sli) => sli.id === column)} />
								{:else if parameters.xChannel === SlicesMetricsOrModels.METRICS}
									{$metrics.find((met) => met.id === column)?.name}
								{:else}
									{column}
								{/if}
							</div>
							<Icon class="material-icons" style="font-size: 25px;">
								{#if sortCol.column === column && sortCol.ascending}
									arrow_drop_up
								{:else if sortCol.column === column}
									arrow_drop_down
								{/if}
							</Icon>
						</div>
					</Cell>
				{/each}
			</Row>
		</Head>
		<Body style="overflow: visible">
			{#each rows as row}
				<TableRow {columns} {tableRecord} {parameters} {row} />
			{/each}
		</Body>
	</DataTable>
</div>
