<script lang="ts">
	import { instanceOfFilterPredicate } from '$lib/api/slice';
	import { getFilteredTable } from '$lib/api/table';
	import {
		columns,
		editTag,
		editedIds,
		model,
		project,
		rowsPerPage,
		selectionIds,
		selectionPredicates,
		selections,
		sort,
		tagIds
	} from '$lib/stores';
	import type { ZenoColumn, ZenoService } from '$lib/zenoapi';
	import { Join, MetadataType, ZenoColumnType } from '$lib/zenoapi';
	import { Icon, Label } from '@smui/button';
	import Checkbox from '@smui/checkbox';
	import { Pagination } from '@smui/data-table';
	import IconButton from '@smui/icon-button';
	import Select, { Option } from '@smui/select';
	import { getContext } from 'svelte';
	import { viewMap } from './views/viewMap';

	export let numberOfInstances = 0;
	export let viewOptions: Record<string, unknown> | undefined;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let tablePromise: Promise<Record<string, string | number | boolean>[]>;
	let columnHeader: ZenoColumn[] = [];
	let currentTagIds: string[] = [];
	let currentPage = 0;
	let lastPage = 0;
	let instanceHidden = false;
	let sampleOptions = [
		...new Set(
			$project.samplesPerPage !== undefined
				? [5, 15, 30, 60, 100, $project.samplesPerPage]
				: [5, 15, 30, 60, 100]
		)
	].sort((a, b) => a - b);

	if ($editTag !== undefined) {
		currentTagIds = $editTag.dataIds;
	}

	$: idColumn = $columns.find((col) => col.columnType === ZenoColumnType.ID)?.id;
	$: dataColumn = $columns.find((col) => col.columnType === ZenoColumnType.DATA)?.id;
	$: labelColumn = $columns.find((col) => col.columnType === ZenoColumnType.LABEL)?.id;

	$: columnHeader = $columns.filter(
		(c) =>
			(c.model === undefined || c.model === null || c.model === $model) &&
			c.columnType === ZenoColumnType.FEATURE
	);
	$: start = currentPage * $rowsPerPage;
	$: end = start + $rowsPerPage;
	$: lastPage = Math.max(Math.ceil(numberOfInstances / $rowsPerPage) - 1, 0);
	$: if (currentPage > lastPage) {
		currentPage = lastPage;
	}
	$: {
		currentTagIds;
		editedIds.set(currentTagIds);
	}
	// update on page, metadata selection, slice selection, or state change.
	$: {
		currentPage;
		$columns;
		$selections.tags;
		$selectionPredicates;
		$model;
		$sort;
		$editTag;
		$rowsPerPage;
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
			predicates,
			zenoClient
		);
	}

	function updateSort(column: ZenoColumn) {
		if ($sort.length < 1 || $sort[0] === undefined || $sort[0].id !== column.id) {
			sort.set([column, true]);
		} else if ($sort[0].id === column.id && $sort[1] === true) {
			sort.set([column, false]);
		} else {
			sort.set([undefined, true]);
		}
	}
</script>

<div class="overflow-y-auto flex flex-wrap content-start w-full h-full">
	<table>
		<thead class="text-left sticky top-0 bg-background cursor-pointer z-10">
			<tr class="border-b border-grey-lighter bg-background">
				{#if $editTag !== undefined}
					<th class="p-3 font-semibold font-grey">Included</th>
				{/if}
				{#if viewMap[$project.view] !== undefined}
					<th
						class="p-3 font-semibold font-grey whitespace-nowrap"
						on:click={() => (instanceHidden = !instanceHidden)}
					>
						instance
						{#if instanceHidden}
							<span class="ml-2 text-grey-darker">hidden</span>
						{/if}
					</th>
				{/if}
				{#each columnHeader as header}
					{#if header.id !== idColumn}
						<th class="p-3 font-semibold font-grey" on:click={() => updateSort(header)}>
							<div class="flex">
								{header.name}
								<Icon
									class="material-icons"
									style="font-size: 14px; padding-top:3px; margin-left: 5px;"
								>
									{#if $sort[0] && $sort[0].name === header.name && $sort[1]}
										keyboard_arrow_down
									{:else if $sort[0] && $sort[0].name === header.name}
										keyboard_arrow_up
									{/if}
								</Icon>
							</div>
						</th>
					{/if}
				{/each}
			</tr>
		</thead>
		<tbody>
			{#await tablePromise then table}
				{#if idColumn}
					{#each table as tableContent (tableContent[idColumn])}
						<tr class="border-b border-grey-lighter">
							{#if $editTag !== undefined}
								<td class="p-3">
									<Checkbox bind:group={currentTagIds} value={String(tableContent[idColumn])} />
								</td>
							{/if}
							{#if viewMap[$project.view] !== undefined}
								<td class="p-3">
									{#if instanceHidden}
										<p class="text-center">...</p>
									{:else}
										<div class="instance">
											<svelte:component
												this={viewMap[$project.view]}
												options={viewOptions}
												entry={tableContent}
												{dataColumn}
												modelColumn={modelColumn?.id}
												{labelColumn}
											/>
										</div>
									{/if}
								</td>
							{/if}
							{#each columnHeader as header}
								{#if header.dataType === MetadataType.CONTINUOUS}
									<td class="p-3 border border-grey-lighter align-top">
										{parseFloat(`${tableContent[header.id]}`).toFixed(2)}
									</td>
								{:else}
									<td class="p-3 border border-grey-lighter align-top">
										{tableContent[header.id]}
									</td>
								{/if}
							{/each}
						</tr>
					{/each}
				{/if}
			{:catch e}
				<p>error loading data: {e}</p>
			{/await}
		</tbody>
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
