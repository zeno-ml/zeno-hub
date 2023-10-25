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
	import { Join, MetadataType, ZenoColumnType, ZenoService, type GroupMetric } from '$lib/zenoapi';
	import { Icon, Label } from '@smui/button';
	import { Pagination } from '@smui/data-table';
	import IconButton from '@smui/icon-button';
	import InstanceView from '@zeno-ml/zeno-instance-views';
	import { getContext } from 'svelte';

	export let modelAResult: Promise<GroupMetric[] | undefined>;
	export let modelBResult: Promise<GroupMetric[] | undefined>;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let tablePromise: Promise<Record<string, string | number | boolean>[]>;
	let instanceContainer: HTMLDivElement;
	// Which model column to show sort for.
	let sortModel = '';
	let currentPage = 0;
	let lastPage = 0;

	let sampleOptions = [
		...new Set(
			$project.samplesPerPage !== undefined
				? [5, 15, 30, 60, 100, $project.samplesPerPage]
				: [5, 15, 30, 60, 100]
		)
	].sort((a, b) => a - b);

	$: idColumn = $columns.find((col) => col.columnType === ZenoColumnType.ID)?.id;
	$: dataColumn = $columns.find((col) => col.columnType === ZenoColumnType.DATA)?.id;
	$: labelColumn = $columns.find((col) => col.columnType === ZenoColumnType.LABEL)?.id;

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
		$model;
		$comparisonModel;
		$comparisonColumn;
		$rowsPerPage;
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

	function updateSort(model: string | undefined) {
		if (model === undefined) return;

		sortModel = model;

		let sortColumnObjects = $columns.filter(
			(col) => col.name == $comparisonColumn?.name && col.model == model
		);

		// if no column found for model, model is "", find col for any model.
		if (sortColumnObjects.length === 0) {
			sortColumnObjects = $columns.filter((col) => col.name == $comparisonColumn?.name);
		}

		// deep copy to not mutate object
		let compareColumnObj = JSON.parse(JSON.stringify(sortColumnObjects[0]));
		// set ID to blank, telling backend to sort by difference.
		if (sortModel === '') {
			compareColumnObj.id = '';
		}

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
		if (
			isNaN(start) ||
			isNaN(end) ||
			end <= start ||
			$model === undefined ||
			$comparisonModel === undefined
		)
			return;

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
			$project.uuid,
			$columns,
			[$model, $comparisonModel],
			$comparisonColumn,
			start,
			end - start,
			$compareSort,
			dataIds,
			zenoClient,
			predicates
		);

		if (instanceContainer) {
			instanceContainer.scrollTop = 0;
		}
	}

	function modelValueAndDiff(
		model: string | undefined,
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
			<th class="p-3 cursor-pointer hover:text-primary" on:click={() => updateSort($model)}>
				<div class="flex">
					<p>A: {$model}</p>
					{#if sortModel === $model}
						<Icon class="material-icons">
							{#if $compareSort[0] && $compareSort[1]}
								arrow_drop_up
							{:else if $compareSort[0]}
								arrow_drop_down
							{/if}
						</Icon>
					{/if}
				</div>
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
			<th
				class="p-3 cursor-pointer hover:text-primary"
				on:click={() => updateSort($comparisonModel)}
			>
				<div class="flex">
					<p>B: {$comparisonModel}</p>
					{#if sortModel === $comparisonModel}
						<Icon class="material-icons">
							{#if $compareSort[0] && $compareSort[1]}
								arrow_drop_up
							{:else if $compareSort[0]}
								arrow_drop_down
							{/if}
						</Icon>
					{/if}
				</div>
				<div>
					<span class="font-normal text-sm mr-3.5 text-grey-dark">
						{$metric ? $metric.name + ':' : ''}
					</span>
					<span class="font-normal mr-3.5 text-primary">
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
			<th class="p-3 cursor-pointer hover:text-primary" on:click={() => updateSort('')}>
				<div class="flex">
					<div>
						<span class="whitespace-nowrap">Difference in</span>
						<span class="text-grey-dark whitespace-nowrap">{$comparisonColumn?.name}</span>
					</div>
					{#if sortModel === ''}
						<Icon class="material-icons">
							{#if $compareSort[0] && $compareSort[1]}
								arrow_drop_up
							{:else if $compareSort[0]}
								arrow_drop_down
							{/if}
						</Icon>
					{/if}
				</div>
			</th>
		</thead>
		{#await tablePromise then table}
			{#if idColumn}
				<tbody>
					{#each table as tableContent (tableContent[idColumn])}
						<tr>
							<td class="p-3 align-baseline">
								<p class="mb-2">
									<span class="text-grey-dark">{$comparisonColumn?.name}:</span>
									{modelValueAndDiff($model, tableContent)}
								</p>
								<div class="instance">
									<InstanceView
										view={$project.view}
										{dataColumn}
										{labelColumn}
										modelColumn={modelAColumn?.id}
										entry={tableContent}
									/>
								</div>
							</td>
							<td class="p-3 align-baseline">
								<p class="mb-2">
									<span class="text-grey-dark">{$comparisonColumn?.name}:</span>
									{modelValueAndDiff($comparisonModel, tableContent)}
								</p>
								<div class="instance">
									<InstanceView
										view={$project.view}
										{dataColumn}
										{labelColumn}
										modelColumn={modelBColumn?.id}
										entry={tableContent}
									/>
								</div>
							</td>
							{#if $model !== undefined && $comparisonModel !== undefined}
								<td class="p-3 align-text-top"
									>{$comparisonColumn?.dataType === MetadataType.CONTINUOUS
										? Number(tableContent['diff']).toFixed(2)
										: tableContent['diff']}
								</td>
							{/if}
						</tr>
					{/each}
				</tbody>
			{/if}
		{:catch e}
			<p>error loading data: {e}</p>
		{/await}
	</table>
</div>

<Pagination slot="paginate" class="pagination">
	<svelte:fragment slot="rowsPerPage">
		<Label>Rows Per Page</Label>
		<select class="ml-2" bind:value={$rowsPerPage}>
			{#each sampleOptions as option}
				<option value={option}>{option}</option>
			{/each}
		</select>
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
