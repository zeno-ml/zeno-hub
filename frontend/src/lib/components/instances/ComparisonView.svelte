<script lang="ts">
	import { instanceOfFilterPredicate } from '$lib/api/slice';
	import { getFilteredTable } from '$lib/api/table';
	import InstanceView from '$lib/instance-views/InstanceView.svelte';
	import {
		columns,
		compareSort,
		comparisonColumn,
		comparisonModel,
		filterSelection,
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
	import { getContext } from 'svelte';

	export let modelAResult: Promise<GroupMetric[] | undefined>;
	export let modelBResult: Promise<GroupMetric[] | undefined>;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let table: Record<string, string | number | boolean>[] = [];
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

	$: idColumn = $columns.find((col) => col.columnType === ZenoColumnType.ID)?.id || '';
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
	)?.id;
	$: modelBColumn = $columns.find(
		(col) => col.columnType === ZenoColumnType.OUTPUT && col.model === $comparisonModel
	)?.id;

	// when state changes update current table view
	$: {
		currentPage;
		$comparisonModel;
		$comparisonColumn;
		$rowsPerPage;
		$compareSort;
		$selectionPredicates;
		$tagIds;
		$selections.tags;
		start;
		end;
		updateTable(true);
	}
	$: {
		$selectionIds;
		$filterSelection;
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

	function updateTable(resetScroll: boolean = false) {
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

		const secureIds = [
			...($tagIds === undefined ? [] : $tagIds),
			...($filterSelection ? $selectionIds : [])
		];
		const dataIds = [...new Set(secureIds)];
		getFilteredTable(
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
		).then((t) => {
			table = t;
			if (resetScroll) instanceContainer.scrollTop = 0;
		});
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

<div class="h-full w-full overflow-auto" bind:this={instanceContainer}>
	<table class="mt-2 w-full min-w-[1000px] table-fixed">
		<colgroup>
			<col style="width: 45%;" />
			<col style="width: 45%;" />
			<col style="width: 10%;" />
		</colgroup>
		<thead
			class="sticky left-0 top-0 z-10 border-b border-grey-lighter bg-background text-left align-top font-semibold"
		>
			<th class="cursor-pointer p-3 hover:text-primary" on:click={() => updateSort($model)}>
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
					<span class="mr-3.5 text-sm font-normal text-grey-dark">
						{$metric ? $metric.name + ':' : ''}
					</span>
					<span class="mr-3.5 font-normal text-primary">
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
				class="cursor-pointer p-3 hover:text-primary"
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
					<span class="mr-3.5 text-sm font-normal text-grey-dark">
						{$metric ? $metric.name + ':' : ''}
					</span>
					<span class="mr-3.5 font-normal text-primary">
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
			<th class="cursor-pointer p-3 hover:text-primary" on:click={() => updateSort('')}>
				<div class="flex">
					<div>
						<span class="whitespace-nowrap">Difference in</span>
						<span class="whitespace-nowrap text-grey-dark">{$comparisonColumn?.name}</span>
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
		<tbody>
			{#each table as tableContent (`${tableContent[idColumn]}_${modelAColumn}_${modelBColumn}`)}
				<tr>
					<td class="p-3 align-baseline">
						<p class="mb-2">
							<span class="text-grey-dark">{$comparisonColumn?.name}:</span>
							{modelValueAndDiff($model, tableContent)}
						</p>
						<InstanceView
							view={$project.view}
							{dataColumn}
							{labelColumn}
							modelColumn={modelAColumn}
							entry={tableContent}
							selectable={$project.editor}
						/>
					</td>
					<td class="p-3 align-baseline">
						<p class="mb-2">
							<span class="text-grey-dark">{$comparisonColumn?.name}:</span>
							{modelValueAndDiff($comparisonModel, tableContent)}
						</p>
						<InstanceView
							view={$project.view}
							{dataColumn}
							{labelColumn}
							modelColumn={modelBColumn}
							entry={tableContent}
							selectable={$project.editor}
						/>
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
