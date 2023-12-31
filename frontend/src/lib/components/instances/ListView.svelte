<script lang="ts">
	import { instanceOfFilterPredicate } from '$lib/api/slice';
	import { getFilteredTable } from '$lib/api/table';
	import InstanceView from '$lib/instance-views/InstanceView.svelte';
	import type { ViewSchema } from '$lib/instance-views/schema';
	import {
		columns,
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
	import { Join, ZenoColumnType, ZenoService } from '$lib/zenoapi';
	import { Label } from '@smui/button';
	import { Pagination } from '@smui/data-table';
	import IconButton from '@smui/icon-button';
	import { getContext } from 'svelte';
	import Select from '../ui/Select.svelte';

	export let numberOfInstances = 0;

	const zenoClient = getContext('zenoClient') as ZenoService;
	const viewSpec = JSON.parse($project.view) as ViewSchema;

	let listContainer: HTMLDivElement;
	let table: Record<string, string | number | boolean>[] = [];
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
		$sort;
		$tagIds;
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
			if (resetScroll) listContainer.scrollTop = 0;
		});
	}
</script>

<div
	class="grid h-full w-full overflow-y-auto"
	style="grid-template-columns: repeat(auto-fill, minmax({viewSpec.size && viewSpec.size === 'large'
		? '800px'
		: '400px'}, 1fr));
	grid-auto-rows: min-content;"
	bind:this={listContainer}
>
	{#each table as inst (`${inst[idColumn]}_${systemColumn}`)}
		<div class="mr-2 mt-2">
			<InstanceView
				view={$project.view}
				{idColumn}
				{dataColumn}
				{labelColumn}
				{systemColumn}
				entry={inst}
				highlighted={$selectionIds.includes(inst[idColumn] + '')}
				on:select={() =>
					$selectionIds?.includes(inst[idColumn] + '')
						? selectionIds.set($selectionIds.filter((id) => id !== inst[idColumn]))
						: selectionIds.set([...$selectionIds, inst[idColumn] + ''])}
				selectable={$project.editor}
			/>
		</div>
	{/each}
</div>
<Pagination slot="paginate" class="pagination border-none">
	<svelte:fragment slot="rowsPerPage">
		<Label>Instances Per Page</Label>
		<Select
			bind:value={$rowsPerPage}
			options={sampleOptions.map((option) => {
				return { value: option, label: option };
			})}
		/>
	</svelte:fragment>
	<svelte:fragment slot="total">
		{(start + 1).toLocaleString()} -
		{Math.min(end, numberOfInstances).toLocaleString()} of
		{numberOfInstances.toLocaleString()}
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
