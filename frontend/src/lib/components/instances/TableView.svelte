<script lang="ts">
	import { instanceOfFilterPredicate } from '$lib/api/slice';
	import { getFilteredTable } from '$lib/api/table';
	import InstanceView from '$lib/instance-views/InstanceView.svelte';
	import {
		columns,
		editTag,
		filterSelection,
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
	import { Pagination } from '@smui/data-table';
	import IconButton from '@smui/icon-button';
	import { getContext } from 'svelte';

	export let numberOfInstances = 0;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let tableContainer: HTMLDivElement;
	let table: Record<string, string | number | boolean>[] = [];
	let columnHeader: ZenoColumn[] = [];
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

	$: idColumn = $columns.find((col) => col.columnType === ZenoColumnType.ID)?.id || '';
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
	// update on page, metadata selection, slice selection, or state change.
	$: {
		currentPage;
		$columns;
		$selections.tags;
		$selectionPredicates;
		$sort;
		$editTag;
		$rowsPerPage;
		updateTable(true);
	}
	$: {
		$selectionIds;
		$filterSelection;
		updateTable();
	}
	$: systemColumn = $columns.find(
		(col) => col.columnType === ZenoColumnType.OUTPUT && col.model === $model
	)?.id;

	// reset page on selection change
	selectionPredicates.subscribe(() => {
		if (currentPage !== 0) {
			currentPage = 0;
		}
	});

	function updateTable(resetScroll: boolean = false) {
		if (isNaN(start) || isNaN(end) || end <= start || !idColumn) return;
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
			$model ? [$model] : [],
			undefined,
			start,
			end - start,
			$sort,
			dataIds,
			zenoClient,
			predicates
		).then((t) => {
			table = t;
			if (resetScroll) tableContainer.scrollTop = 0;
		});
	}

	function updateSort(column: ZenoColumn) {
		if ($sort.length < 1 || $sort[0] === undefined || $sort[0].id !== column.id) {
			sort.set([column, true]);
		} else if ($sort[0].id === column.id && $sort[1] === true) {
			sort.set([column, false]);
		} else {
			sort.set([undefined, true]);
		}
		currentPage = 0;
	}
</script>

<div class="w-full overflow-auto" bind:this={tableContainer}>
	<table>
		<thead class="sticky top-0 z-10 cursor-pointer bg-background text-left">
			<tr class="border-b border-grey-lighter bg-background">
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
			{#each table as tableContent (`${tableContent[idColumn]}_${systemColumn}`)}
				<tr class="border-b border-grey-lighter">
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
										{systemColumn}
										entry={tableContent}
										selectable={$project.editor}
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
