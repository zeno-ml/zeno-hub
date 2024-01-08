<script lang="ts">
	import {
		SlicesMetricsOrModels,
		SlicesOrModels,
		ZenoService,
		type Chart,
		type Metric,
		type Slice,
		type TableParameters
	} from '$lib/zenoapi';
	import { Icon } from '@smui/button';
	import DataTable, { Body, Cell, Head, Row } from '@smui/data-table';
	import { getContext } from 'svelte';
	import SliceDetailsContainer from './SliceDetailsContainer.svelte';
	import TableRow from './TableRow.svelte';

	export let chart: Chart;
	export let preview: boolean;
	export let data: {
		table: Array<{
			x_value: string | number;
			y_value: string | number;
			fixed_value: number;
			size: number;
		}>;
	};

	const zenoClient = getContext('zenoClient') as ZenoService;

	let metrics: Metric[] = [];
	let slices: Slice[] = [];
	zenoClient.getMetrics(chart.projectUuid).then((met) => {
		metrics = met;
	});
	zenoClient.getSlices(chart.projectUuid).then((sli) => {
		slices = sli;
	});
	let tableRecord: Record<
		string | number,
		Record<string | number, { fixedValue: number; size: number }>
	> = {};
	let sortCol: { column: string | number | undefined; ascending: boolean } = {
		column: undefined,
		ascending: true
	};

	$: parameters = chart.parameters as TableParameters;
	$: columns = [...new Set(data.table.map((cell) => cell.x_value))];
	$: rows = [...new Set(data.table.map((cell) => cell.y_value))];
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

	function saveCSV() {
		let csvContent = 'data:text/csv;charset=utf-8,';
		const cols = columns.map((column) => {
			if (parameters.xChannel === SlicesMetricsOrModels.SLICES) {
				if (column == -1) {
					return 'all instances';
				}
				return slices.find((sli) => sli.id === column)?.sliceName ?? '';
			} else if (parameters.xChannel === SlicesMetricsOrModels.METRICS) {
				return column == -1 ? 'count' : metrics.find((met) => met.id === column)?.name ?? '';
			} else {
				return column;
			}
		});
		csvContent += parameters.yChannel === SlicesOrModels.SLICES ? 'slice' : 'system';
		csvContent += ',';
		csvContent += cols.join(',') + '\n';
		rows.forEach((row) => {
			if (parameters.yChannel === SlicesOrModels.SLICES) {
				if (row == -1) {
					csvContent += 'all instances';
				} else {
					csvContent += slices.find((sli) => sli.id === row)?.sliceName ?? '';
				}
			} else {
				csvContent += row;
			}
			csvContent += ',';
			columns.forEach((column) => {
				csvContent += tableRecord[column][row].fixedValue + ',';
			});
			csvContent = csvContent.slice(0, -1);
			csvContent += '\n';
		});
		const encodedUri = encodeURI(csvContent);
		const link = document.createElement('a');
		link.setAttribute('href', encodedUri);
		link.setAttribute('download', chart.name + '.csv');
		document.body.appendChild(link);
		link.click();
	}
</script>

<div class="my-2">
	<DataTable>
		<Head>
			<Row>
				<Cell>{parameters.yChannel === SlicesOrModels.SLICES ? 'slices' : 'systems'}</Cell>
				{#each columns as column}
					<Cell
						class="pointer"
						on:keydown={() => ({})}
						on:click={() => {
							if (sortCol.column !== column) {
								sortCol = { column: column, ascending: true };
							} else if (sortCol.ascending) {
								sortCol = { ...sortCol, ascending: !sortCol.ascending };
							} else {
								sortCol = { column: undefined, ascending: true };
							}
						}}
					>
						<div class="flex cursor-pointer transition hover:text-primary-dark">
							<div class="min-h-[24px] overflow-hidden">
								{#if parameters.xChannel === SlicesMetricsOrModels.SLICES}
									<SliceDetailsContainer sli={slices.find((sli) => sli.id === column)} />
								{:else if parameters.xChannel === SlicesMetricsOrModels.METRICS}
									{column == -1 ? 'count' : metrics.find((met) => met.id === column)?.name}
								{:else}
									{column}
								{/if}
							</div>
							<Icon class="material-icons">
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
		<Body>
			{#each rows as row}
				<TableRow {columns} {slices} {tableRecord} {parameters} {row} />
			{/each}
		</Body>
	</DataTable>
</div>
{#if !preview}
	<button
		on:click={saveCSV}
		class="ml-auto rounded border border-primary-dark px-2 py-0.5 text-primary transition hover:bg-primary-mid"
	>
		Download CSV
	</button>
{/if}
