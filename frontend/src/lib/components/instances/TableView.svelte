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
	import InstanceView from '@zeno-ml/zeno-instance-views';
	import { getContext } from 'svelte';

	export let numberOfInstances = 0;

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
			(c.columnType === ZenoColumnType.FEATURE ||
				((c.columnType === ZenoColumnType.LABEL || c.columnType === ZenoColumnType.OUTPUT) &&
					$project.view == ''))
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
			zenoClient,
			predicates
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

<div class="w-full overflow-auto">
	<table>
		<thead class="sticky top-0 z-10 cursor-pointer bg-background text-left">
			<tr class="border-b border-grey-lighter bg-background">
				{#if $editTag !== undefined}
					<th class="font-grey p-3 font-semibold">Included</th>
				{/if}
				<th class="font-grey p-3 font-semibold">ID</th>
				{#if $project.view}
					<th
						class="font-grey whitespace-nowrap p-3 font-semibold"
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
						<th class="font-grey p-3 font-semibold" on:click={() => updateSort(header)}>
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
							<td class="border border-grey-lighter p-3 align-top">
								{tableContent[idColumn]}
							</td>
							{#if $project.view}
								<td class="p-3">
									{#if instanceHidden}
										<p class="text-center">...</p>
									{:else}
										<div class="instance">
											<InstanceView
												view={$project.view}
												{dataColumn}
												{labelColumn}
												modelColumn={modelColumn?.id}
												entry={tableContent}
											/>
										</div>
									{/if}
								</td>
							{/if}
							{#each columnHeader as header}
								{#if header.dataType === MetadataType.CONTINUOUS}
									<td class="border border-grey-lighter p-3 align-top">
										{parseFloat(`${tableContent[header.id]}`).toFixed(2)}
									</td>
								{:else}
									<td class="border border-grey-lighter p-3 align-top">
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
		<select class="ml-2" bind:value={$rowsPerPage}>
			{#each sampleOptions as option}
				<option value={option}>{option}</option>
			{/each}
		</select>
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
