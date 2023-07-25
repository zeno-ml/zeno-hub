<script lang="ts">
	import { browser } from '$app/environment';
	import { instanceOfFilterPredicate, setModelForFilterPredicateGroup } from '$lib/api/slice';
	import { getFilteredTable } from '$lib/api/table';
	import {
		columns,
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
	import { Join, ZenoColumnType, type GroupMetric } from '$lib/zenoapi';
	import { Label } from '@smui/button';
	import { Pagination } from '@smui/data-table';
	import IconButton from '@smui/icon-button';
	import Select, { Option } from '@smui/select';
	import { viewMap } from './views/viewMap';

	export let currentResult: GroupMetric[] | undefined;
	export let viewOptions: Record<string, unknown> | undefined;

	let table: Record<string, string | number | boolean>[];

	let currentPage = 0;
	let lastPage = 0;

	let sampleOptions = [
		...new Set(
			$projectConfig !== undefined && $projectConfig.numItems !== undefined
				? [5, 15, 30, 60, 100, $projectConfig.numItems]
				: [5, 15, 30, 60, 100]
		)
	].sort((a, b) => a - b);

	$: start = currentPage * $rowsPerPage;
	$: end = start + $rowsPerPage;
	$: if (currentResult !== undefined) {
		lastPage = Math.max(Math.ceil(currentResult[0].size / $rowsPerPage) - 1, 0);
	}
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
</script>

{#if table}
	{#if $projectConfig !== undefined && viewMap[$projectConfig.view] !== undefined}
		<div class="container sample-container">
			{#each table as inst (inst['item'])}
				<div class="instance">
					<svelte:component
						this={viewMap[$projectConfig.view]}
						options={viewOptions}
						entry={{
							...inst,
							data: `${getEndpoint()}/api/data/${$projectConfig.uuid}?item=${encodeURIComponent(
								inst['item']
							)}`
						}}
						modelColumn={modelColumn?.id}
					/>
				</div>
			{/each}
		</div>
	{/if}
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

<style>
	.sample-container {
		height: calc(100vh - 180px);
		overflow-y: auto;
		align-content: baseline;
		border-bottom: 1px solid rgb(224, 224, 224);
		display: flex;
		flex-wrap: wrap;
	}
	.instance {
		margin-right: 5px;
		margin-top: 2.5px;
		margin-bottom: 2.5px;
	}
</style>
