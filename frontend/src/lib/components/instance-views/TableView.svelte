<script lang="ts">
	import { browser } from '$app/environment';
	import { instanceOfFilterPredicate, setModelForFilterPredicateGroup } from '$lib/api/slice';
	import { getFilteredTable } from '$lib/api/table';
	import {
		columns,
		editTag,
		editedIds,
		model,
		projectConfig,
		rowsPerPage,
		selectionIds,
		selectionPredicates,
		selections,
		sort,
		tagIds
	} from '$lib/stores';
	import { getEndpoint } from '$lib/util/util';
	import type { GroupMetric, ZenoColumn } from '$lib/zenoapi';
	import { Join, MetadataType, ZenoColumnType } from '$lib/zenoapi';
	import { Icon, Label } from '@smui/button';
	import Checkbox from '@smui/checkbox';
	import { Pagination } from '@smui/data-table';
	import IconButton from '@smui/icon-button';
	import Select, { Option } from '@smui/select';
	import { viewMap } from './views/viewMap';

	export let currentResult: GroupMetric[] | undefined;
	export let viewOptions: Record<string, unknown> | undefined;

	let table: Record<string, string | number | boolean>[];
	let columnHeader: ZenoColumn[] = [];
	let currentTagIds: string[] = [];
	let currentPage = 0;
	let lastPage = 0;
	let sampleOptions = [
		...new Set(
			$projectConfig !== undefined && $projectConfig.numItems !== undefined
				? [5, 15, 30, 60, 100, $projectConfig.numItems]
				: [5, 15, 30, 60, 100]
		)
	].sort((a, b) => a - b);

	if ($editTag !== undefined) {
		currentTagIds = $editTag.items;
	}

	$: columnHeader = $columns.filter(
		(c) =>
			(c.model === undefined || c.model === null || c.model === $model) &&
			(c.columnType === ZenoColumnType.METADATA ||
				c.columnType === ZenoColumnType.PREDISTILL ||
				c.columnType === ZenoColumnType.POSTDISTILL)
	);
	$: start = currentPage * $rowsPerPage;
	$: end = start + $rowsPerPage;
	$: if (currentResult !== undefined) {
		lastPage = Math.max(Math.ceil(currentResult[0].size / $rowsPerPage) - 1, 0);
	}
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
		if (currentPage === 0) {
			updateTable();
		} else {
			currentPage = 0;
		}
	});

	function updateTable() {
		if (!browser || isNaN(start) || isNaN(end) || end <= start) return;
		if ($model !== undefined) {
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
			const items = [...new Set([...secureTagIds, ...secureSelectionIds])];
			getFilteredTable(
				$columns,
				[$model],
				undefined,
				start,
				end - start,
				$sort,
				items,
				predicates
			).then((res) => (table = res));
		}
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

{#if table}
	<div class="overflow-auto flex flex-wrap content-baseline">
		<table id="column-table">
			<thead
				class="border-b-2 border-grey-lighter text-left pb-1 mb-5 sticky top-0 bg-background cursor-pointer"
			>
				<tr>
					{#if $editTag !== undefined}
						<th class="mr-5">Included</th>
					{/if}
					{#if $projectConfig !== undefined && viewMap[$projectConfig.view] !== undefined}
						<th class="mr-5">instance</th>
					{/if}
					{#each columnHeader as header}
						{#if header.name !== 'item'}
							<th class="mr-5" on:click={() => updateSort(header)}>
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
				{#each table as tableContent (tableContent['item'])}
					<tr>
						{#if $editTag !== undefined}
							<td class="pr-3.5"
								><Checkbox bind:group={currentTagIds} value={String(tableContent['item'])} /></td
							>
						{/if}
						{#if $projectConfig !== undefined && viewMap[$projectConfig.view] !== undefined}
							<td class="pr-3.5">
								<div class="instance">
									<svelte:component
										this={viewMap[$projectConfig.view]}
										options={viewOptions}
										entry={{
											...tableContent,
											data: `${getEndpoint()}/api/data/${
												$projectConfig.uuid
											}?item=${encodeURIComponent(tableContent['item'])}`
										}}
										modelColumn={modelColumn?.id}
									/>
								</div>
							</td>
						{/if}
						{#each columnHeader as header}
							{#if header.dataType === MetadataType.CONTINUOUS}
								<td class="pr-3.5">{parseFloat(`${tableContent[header.id]}`).toFixed(2)}</td>
							{:else}
								<td class="pr-3.5">{tableContent[header.id]}</td>
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
			<Select variant="outlined" bind:value={$rowsPerPage} noLabel>
				{#each sampleOptions as option}
					<Option value={option}>{option}</Option>
				{/each}
			</Select>
		</svelte:fragment>
		<svelte:fragment slot="total">
			{start + 1}-
			{Math.min(end, currentResult ? currentResult[0].size : end)} of
			{currentResult ? currentResult[0].size : ''}
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
{/if}
