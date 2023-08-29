<script lang="ts">
	import { browser } from '$app/environment';
	import { instanceOfFilterPredicate, setModelForFilterPredicateGroup } from '$lib/api/slice';
	import { getFilteredTable } from '$lib/api/table';
	import {
		columns,
		compareSort,
		comparisonColumn,
		comparisonModel,
		metric,
		model,
		models,
		project,
		rowsPerPage,
		selectionIds,
		selectionPredicates,
		selections,
		tagIds
	} from '$lib/stores';
	import { Join, MetadataType, ZenoColumnType, type GroupMetric } from '$lib/zenoapi';
	import { Label } from '@smui/button';
	import { Pagination } from '@smui/data-table';
	import IconButton from '@smui/icon-button';
	import Select, { Option } from '@smui/select';
	import ComparisonViewTableHeader from './ComparisonViewTableHeader.svelte';
	import { viewMap } from './views/viewMap';

	export let viewOptions: Record<string, unknown> | undefined;
	export let modelAResult: GroupMetric[] | undefined;
	export let modelBResult: GroupMetric[] | undefined;

	let table: Record<string, string | number | boolean>[] | undefined;
	let instanceContainer: HTMLDivElement;

	// decide which model column to show sort icon
	let sortModel = '';

	let currentPage = 0;
	let lastPage = 0;
	let metricA = 0;
	let metricB = 0;

	let sampleOptions = [
		...new Set(
			$project !== undefined && $project.samplesPerPage !== undefined
				? [5, 15, 30, 60, 100, $project.samplesPerPage]
				: [5, 15, 30, 60, 100]
		)
	].sort((a, b) => a - b);

	$: start = currentPage * $rowsPerPage;
	$: end = start + $rowsPerPage;
	$: if (currentPage > lastPage) {
		currentPage = lastPage;
	}
	$: if (modelAResult !== undefined) {
		lastPage = Math.max(Math.ceil(modelAResult[0].size / $rowsPerPage) - 1, 0);
		if (modelAResult[0].metric !== undefined && modelAResult[0].metric !== null)
			metricA = Math.round(modelAResult[0].metric * 100) / 100;
	}
	$: if (modelBResult !== undefined) {
		lastPage = Math.max(Math.ceil(modelBResult[0].size / $rowsPerPage) - 1, 0);
		if (modelBResult[0].metric !== undefined && modelBResult[0].metric !== null)
			metricA = Math.round(modelBResult[0].metric * 100) / 100;
	}
	$: modelAColumn = $columns.find(
		(col) => col.columnType === ZenoColumnType.OUTPUT && col.model === $model
	);
	$: modelBColumn = $columns.find(
		(col) => col.columnType === ZenoColumnType.OUTPUT && col.model === $comparisonModel
	);
	// when state changes update current table view
	$: {
		currentPage;
		$comparisonModel;
		$rowsPerPage;
		$model;
		$comparisonModel;
		$compareSort;
		$selectionIds;
		$selectionPredicates;
		$tagIds;
		$selections.tags;
		start, end;
		updateTable();
	}

	comparisonColumn.subscribe((_) => {
		table = undefined;
		compareSort.set([undefined, true]);
	});

	model.subscribe((model) => {
		// make sure Model A and Model B are exclusive
		if ($comparisonModel && $comparisonModel === model) {
			$comparisonModel = $models.filter((m) => m !== model)[0];
		}
	});

	// reset page on selection change
	selectionPredicates.subscribe(() => {
		if (currentPage !== 0) {
			currentPage = 0;
		}
	});

	// trigger this function when clicking column header to sort
	function updateSort(model: string | undefined) {
		if (model === undefined) return;
		// when clicking different model columns, reset compareSort
		if (sortModel !== model) {
			compareSort.set([undefined, true]);
			sortModel = model;
		}

		// assign new model to the selected column
		let newHeader = setColumnModel(model);

		let compareSortString = JSON.stringify($compareSort[0]);
		let newHeaderString = JSON.stringify(newHeader);

		if (compareSortString !== newHeaderString) {
			compareSort.set([newHeader, true]);
		} else if (compareSortString === newHeaderString && $compareSort[1]) {
			compareSort.set([newHeader, false]);
		} else {
			compareSort.set([undefined, true]);
		}
	}

	// set model for feature/output column
	function setColumnModel(model: string) {
		let col_copy = Object.assign({}, $comparisonColumn);
		col_copy.model =
			(col_copy.columnType === ZenoColumnType.FEATURE &&
				col_copy.model !== undefined &&
				col_copy.model !== null) ||
			col_copy.columnType === ZenoColumnType.OUTPUT
				? model
				: '';
		return col_copy;
	}

	function updateTable() {
		if (!browser || isNaN(start) || isNaN(end) || end <= start) return;
		if ($model !== undefined && $comparisonModel !== undefined) {
			let predicates =
				$selectionPredicates === undefined
					? undefined
					: setModelForFilterPredicateGroup($selectionPredicates, $model);
			if (predicates !== undefined && instanceOfFilterPredicate(predicates)) {
				predicates = {
					join: Join._,
					predicates: [predicates]
				};
			}
			const secureTagIds = $tagIds === undefined ? [] : $tagIds;
			const secureSelectionIds = $selectionIds === undefined ? [] : $selectionIds;
			const dataIds = [...new Set([...secureTagIds, ...secureSelectionIds])];
			getFilteredTable(
				$columns,
				[$model, $comparisonModel],
				$comparisonColumn,
				start,
				end - start,
				$compareSort,
				dataIds,
				predicates
			).then((res) => {
				table = res;
				if (instanceContainer) {
					instanceContainer.scrollTop = 0;
				}
			});
		}
	}

	function modelValueAndDiff(
		model: string,
		diff: boolean,
		tableContent: Record<string, string | number | boolean>
	) {
		let newHeader = setColumnModel(model);
		let key = diff ? 'diff' : newHeader.id;
		return tableContent[key] && newHeader.dataType === MetadataType.CONTINUOUS
			? parseFloat(`${tableContent[key]}`).toFixed(2)
			: tableContent[key];
	}
</script>

<div class="w-full overflow-auto" bind:this={instanceContainer}>
	{#if table}
		<table class="mt-2">
			<thead
				class="sticky border-b border-grey-lighter font-semibold top-0 left-0 text-left align-top bg-background z-10"
			>
				<th class="p-3">
					<div>A: {$model}</div>
					<div>
						<span class="font-normal text-sm mr-3.5 text-grey-dark">
							{$metric ? $metric.name + ':' : ''}
						</span>
						<span class="font-normal mr-3.5 text-primary">
							{metricA}
						</span>
					</div>
				</th>
				<th class="p-3">
					<div>B: {$comparisonModel}</div>
					<div>
						<span class="font-normal text-sm mr-3.5 text-grey-dark">
							{$metric ? $metric.name + ':' : ''}
						</span>
						<span class="font-normal text-sm mr-3.5 text-primary">
							{metricB}
						</span>
					</div>
				</th>
				<th on:click={() => updateSort($model)} class="cursor-pointer p-3 min-width-[200px]">
					<ComparisonViewTableHeader {sortModel} header={$model} />
				</th>
				<th
					on:click={() => updateSort($comparisonModel)}
					class="cursor-pointer p-3 min-width-[200px]"
				>
					<ComparisonViewTableHeader {sortModel} header={$comparisonModel} />
				</th>
				<th on:click={() => updateSort('')} class="cursor-pointer p-3 min-width-[200px]">
					<ComparisonViewTableHeader {sortModel} header={''} />
				</th>
			</thead>
			<tbody>
				{#each table as tableContent}
					<tr>
						{#if $project !== undefined && viewMap[$project.view] !== undefined}
							<td class="pr-2.5">
								<div class="instance">
									<svelte:component
										this={viewMap[$project.view]}
										options={viewOptions}
										entry={tableContent}
										modelColumn={modelAColumn?.id}
									/>
								</div>
							</td>
							<td class="pr-2.5">
								<div class="instance">
									<svelte:component
										this={viewMap[$project.view]}
										options={viewOptions}
										entry={tableContent}
										modelColumn={modelBColumn?.id}
									/>
								</div>
							</td>
						{/if}
						{#if $model !== undefined && $comparisonModel !== undefined}
							<td class="pr-2.5">{modelValueAndDiff($model, false, tableContent)}</td>
							<td class="pr-2.5">{modelValueAndDiff($comparisonModel, false, tableContent)}</td>
							<td class="pr-2.5">{modelValueAndDiff($model, true, tableContent)}</td>
						{/if}
					</tr>
				{/each}
			</tbody>
		</table>
	{/if}
</div>

<Pagination slot="paginate" class="pagination">
	<svelte:fragment slot="rowsPerPage">
		<Label>Rows Per Page</Label>
		<Select variant="outlined" bind:value={$rowsPerPage} noLabel>
			{#each sampleOptions as option}
				<Option value={option}>{option}</Option>
			{/each}
		</Select>
	</svelte:fragment>
	<svelte:fragment slot="total">
		{start + 1}-
		{Math.min(end, modelAResult ? modelAResult[0].size : end)} of
		{modelAResult ? modelAResult[0].size : ''}
	</svelte:fragment>

	<IconButton
		class="material-icons"
		action="first-page"
		title="First page"
		on:click={() => (currentPage = 0)}
		disabled={currentPage === 0}>first_page</IconButton
	>
	<IconButton
		class="material-icons"
		action="prev-page"
		title="Prev page"
		on:click={() => currentPage--}
		disabled={currentPage === 0}>chevron_left</IconButton
	>
	<IconButton
		class="material-icons"
		action="next-page"
		title="Next page"
		on:click={() => currentPage++}
		disabled={currentPage >= lastPage}>chevron_right</IconButton
	>
	<IconButton
		class="material-icons"
		action="last-page"
		title="Last page"
		on:click={() => (currentPage = lastPage)}
		disabled={currentPage >= lastPage}>last_page</IconButton
	>
</Pagination>
