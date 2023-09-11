<script lang="ts">
	import { instanceOfFilterPredicate } from '$lib/api/slice';
	import { getFilteredTable } from '$lib/api/table';
	import {
		columns,
		compareSort,
		comparisonColumn,
		comparisonModel,
		metric,
		model,
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
	export let modelAResult: Promise<GroupMetric[] | undefined>;
	export let modelBResult: Promise<GroupMetric[] | undefined>;

	let tablePromise: Promise<Record<string, string | number | boolean>[]>;
	let instanceContainer: HTMLDivElement;

	// Which model column to show sort for.
	let sortModel = '';
	let currentPage = 0;
	let lastPage = 0;

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
	$: modelAResult.then((r) => {
		if (r !== undefined && r.length > 0) {
			lastPage = Math.max(Math.ceil(r[0].size / $rowsPerPage) - 1, 0);
		}
	});

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
		$comparisonColumn;
		$rowsPerPage;
		$model;
		$compareSort;
		$selectionIds;
		$selectionPredicates;
		$tagIds;
		$selections.tags;
		start;
		end;
		updateTable();
	}

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

		let compareColumnObj = $columns.filter(
			(col) => col.name == $comparisonColumn?.name && col.model == $comparisonModel
		)[0];

		let compareSortString = JSON.stringify($compareSort[0]);
		let newHeaderString = JSON.stringify(compareColumnObj);

		if (compareSortString !== newHeaderString) {
			compareSort.set([compareColumnObj, true]);
		} else if (compareSortString === newHeaderString && $compareSort[1]) {
			compareSort.set([compareColumnObj, false]);
		} else {
			compareSort.set([undefined, true]);
		}
	}

	function updateTable() {
		if (isNaN(start) || isNaN(end) || end <= start) return;
		if ($model !== undefined && $comparisonModel !== undefined) {
			let predicates = $selectionPredicates;
			if (predicates !== undefined && instanceOfFilterPredicate(predicates)) {
				predicates = {
					join: Join._,
					predicates: [predicates]
				};
			}
			const secureTagIds = $tagIds === undefined ? [] : $tagIds;
			const secureSelectionIds = $selectionIds === undefined ? [] : $selectionIds;
			const dataIds = [...new Set([...secureTagIds, ...secureSelectionIds])];
			tablePromise = getFilteredTable(
				$columns,
				[$model, $comparisonModel],
				$comparisonColumn,
				start,
				end - start,
				$compareSort,
				dataIds,
				predicates
			);
			if (instanceContainer) {
				instanceContainer.scrollTop = 0;
			}
		}
	}

	function modelValueAndDiff(
		model: string,
		tableContent: Record<string, string | number | boolean>
	) {
		const compareColumnObj = $columns.filter(
			(col) => col.name == $comparisonColumn?.name && col.model == model
		)[0];
		const id = compareColumnObj.id;
		return compareColumnObj.dataType === MetadataType.CONTINUOUS
			? parseFloat(`${tableContent[id]}`).toFixed(2)
			: tableContent[id];
	}
</script>

<div class="w-full h-full overflow-auto" bind:this={instanceContainer}>
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
						{#await modelAResult then res}
							{#if res !== undefined && res.length > 0}
								{#if res[0].metric !== undefined && res[0].metric !== null}
									{res[0].metric.toFixed(2)}
								{/if}
							{/if}
						{/await}
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
						{#await modelBResult then res}
							{#if res !== undefined && res.length > 0}
								{#if res[0].metric !== undefined && res[0].metric !== null}
									{res[0].metric.toFixed(2)}
								{/if}
							{/if}
						{/await}
					</span>
				</div>
			</th>
			<th on:click={() => updateSort($model)} class="cursor-pointer p-3 min-w-[150px]">
				<ComparisonViewTableHeader {sortModel} header={$model} />
			</th>
			<th on:click={() => updateSort($comparisonModel)} class="cursor-pointer p-3 min-w-[150px]">
				<ComparisonViewTableHeader {sortModel} header={$comparisonModel} />
			</th>
			<th on:click={() => updateSort('')} class="cursor-pointer p-3 min-w-[150px]">
				<ComparisonViewTableHeader {sortModel} header={''} />
			</th>
		</thead>
		{#await tablePromise then table}
			<tbody>
				{#each table as tableContent}
					<tr>
						{#if $project !== undefined && viewMap[$project.view] !== undefined}
							<td class="p-3 align-baseline">
								<div class="instance">
									<svelte:component
										this={viewMap[$project.view]}
										options={viewOptions}
										entry={tableContent}
										modelColumn={modelAColumn?.id}
									/>
								</div>
							</td>
							<td class="p-3 align-baseline">
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
							<td class="p-3 align-text-top">{modelValueAndDiff($model, tableContent)}</td>
							<td class="p-3 align-text-top">{modelValueAndDiff($comparisonModel, tableContent)}</td
							>
							<td class="p-3 align-text-top"
								>{Number(tableContent['diff'])
									? Number(tableContent['diff']).toFixed(2)
									: tableContent['diff']}</td
							>
						{/if}
					</tr>
				{/each}
			</tbody>
		{:catch e}
			<p>error loading data: {e}</p>
		{/await}
	</table>
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
		{start + 1} -
		{#await modelAResult then res}
			{Math.min(end, res ? res[0].size : end)} of
			{res ? res[0].size : ''}
		{/await}
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
