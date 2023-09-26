<script lang="ts">
	import { instanceOfFilterPredicate } from '$lib/api/slice';
	import { getFilteredTable } from '$lib/api/table';
	import {
		columns,
		model,
		project,
		rowsPerPage,
		selectionIds,
		selectionPredicates,
		selections,
		sort,
		tagIds
	} from '$lib/stores';
	import { Join, ZenoColumnType } from '$lib/zenoapi';
	import { Label } from '@smui/button';
	import { Pagination } from '@smui/data-table';
	import IconButton from '@smui/icon-button';
	import Select, { Option } from '@smui/select';
	import { viewMap } from './views/viewMap';

	export let numberOfInstances = 0;
	export let viewOptions: Record<string, unknown> | undefined;

	let tablePromise: Promise<Record<string, string | number | boolean>[]>;

	let currentPage = 0;
	let lastPage = 0;

	let sampleOptions = [
		...new Set(
			$project.samplesPerPage !== undefined
				? [5, 15, 30, 60, 100, $project.samplesPerPage]
				: [5, 15, 30, 60, 100]
		)
	].sort((a, b) => a - b);

	$: start = currentPage * $rowsPerPage;
	$: end = start + $rowsPerPage;
	$: lastPage = Math.max(Math.ceil(numberOfInstances / $rowsPerPage) - 1, 0);

	$: if (currentPage > lastPage) {
		currentPage = lastPage;
	}

	// when state changes update current table view
	$: {
		currentPage;
		$rowsPerPage;
		$columns;
		$selections.tags;
		$model;
		$sort;
		$tagIds;
		$selectionIds;
		updateTable();
	}

	$: modelColumn = $columns.find(
		(col) => col.columnType === ZenoColumnType.OUTPUT && col.model === $model
	);

	// reset page on selection change
	selectionPredicates.subscribe(() => {
		if (currentPage !== 0) {
			currentPage = 0;
		}
	});

	function updateTable() {
		if (isNaN(start) || isNaN(end) || end <= start) return;
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
			$model ? [$model] : [],
			undefined,
			start,
			end - start,
			$sort,
			dataIds,
			predicates
		);
	}
</script>

<div class="overflow-y-auto flex flex-wrap content-start w-full h-full">
	{#await tablePromise then table}
		{#if viewMap[$project.view] !== undefined}
			{#each table as inst (inst['data_id'])}
				<div class="mr-2 mt-2">
					<svelte:component
						this={viewMap[$project.view]}
						options={viewOptions}
						entry={inst}
						modelColumn={modelColumn?.id}
					/>
				</div>
			{/each}
		{/if}
	{:catch e}
		<p>error loading data: {e}</p>
	{/await}
</div>
<Pagination slot="paginate" class="pagination">
	<svelte:fragment slot="rowsPerPage">
		<Label>Instances Per Page</Label>
		<Select variant="outlined" bind:value={$rowsPerPage} noLabel>
			{#each sampleOptions as option}
				<Option value={option}>{option}</Option>
			{/each}
		</Select>
	</svelte:fragment>
	<svelte:fragment slot="total">
		{start + 1} -
		{Math.min(end, numberOfInstances)} of
		{numberOfInstances}
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
