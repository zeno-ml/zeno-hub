<script lang="ts">
	import { page } from '$app/stores';
	import {
		columns,
		comparisonModel,
		filterSelection,
		model,
		project,
		selectionIds,
		selectionPredicates,
		selections,
		tagIds
	} from '$lib/stores';
	import { tooltip } from '$lib/util/tooltip';
	import { columnSort, svelecteRenderer } from '$lib/util/util';
	import {
		MetadataType,
		ZenoColumnType,
		type SliceFinderReturn,
		type ZenoColumn,
		type ZenoService
	} from '$lib/zenoapi';
	import { mdiClose, mdiInformationOutline } from '@mdi/js';
	import Button from '@smui/button';
	import IconButton, { Icon } from '@smui/icon-button';
	import Svelecte from 'svelecte';
	import { createEventDispatcher, getContext } from 'svelte';
	import ChipsWrapper from '../metadata/ChipsWrapper.svelte';
	import SliceFinderCell from '../metadata/cells/SliceFinderCell.svelte';
	import Popup from './Popup.svelte';

	const dispatch = createEventDispatcher();
	const zenoClient = getContext('zenoClient') as ZenoService;

	let blur = function (ev: CustomEvent<unknown>) {
		ev.target !== null && (ev.target as HTMLElement).blur();
	};

	let completeColumns = $columns.filter(
		(d) =>
			(d.columnType === ZenoColumnType.FEATURE || d.columnType === ZenoColumnType.OUTPUT) &&
			(d.model === undefined || d.model === null || d.model === $model)
	);

	// Columns to create candidate slices accross
	let searchColumnOptions = $columns.filter(
		(d) =>
			d.dataType !== MetadataType.OTHER &&
			d.dataType !== MetadataType.DATETIME &&
			completeColumns.includes(d)
	);
	let modelFeatureColumns = searchColumnOptions.filter(
		(col) =>
			col.columnType === ZenoColumnType.FEATURE && col.model !== null && col.model !== undefined
	);
	let searchColumns =
		modelFeatureColumns.length > 0 ? modelFeatureColumns : [searchColumnOptions[0]];

	// Column to use as the metric to compare slices.
	let metricColumns = $columns
		.filter((d) => {
			return $page.url.href.includes('compare')
				? (d.columnType === ZenoColumnType.OUTPUT || d.columnType === ZenoColumnType.FEATURE) &&
						d.model === $model
				: (d.dataType === MetadataType.CONTINUOUS || d.dataType === MetadataType.BOOLEAN) &&
						completeColumns.includes(d);
		})
		.sort(columnSort);
	let metricColumn: ZenoColumn | undefined =
		metricColumns.length > 0 ? metricColumns[0] : undefined;
	let compareColumn: ZenoColumn | undefined = undefined;
	$: if (metricColumn && $page.url.href.includes('compare')) {
		compareColumn = Object.assign({}, metricColumn);
		if (compareColumn.model) {
			compareColumn.model = $comparisonModel;
		}
	}

	let alphas = ['0.5', '0.75', '0.9', '0.95', '0.99', '0.999'];
	let alphaIdx = 4;
	let maxlattice = ['1', '2', '3', '4', '5', '6'];
	let maxlatticeIdx = 3;
	let orderByOptions = ['descending', 'ascending'];
	let compareOrderByOptions = ['(system) A > B', '(system) B > A'];
	let orderByIdx = $page.url.href.includes('compare') ? 1 : 0;

	let sliceFinderReturn = {
		slices: [],
		metrics: [],
		sizes: [],
		overallMetric: undefined
	} as SliceFinderReturn;

	$: sliceFinderMessage = '';

	/** Run sliceline algorithm to generate recommended slices **/
	export async function generateSlices() {
		if (searchColumns.length === 0 || metricColumn === null) {
			sliceFinderMessage = 'Must have a metric column and at least one search column.';
			return;
		}
		if (alphaIdx === null || maxlattice === null || orderByIdx === null) {
			sliceFinderMessage = "Parameters (Alpha, Max. Lattice, Order By) can't be null.";
			return;
		}
		sliceFinderMessage = 'Generating Slices...';
		if (metricColumn !== undefined) {
			const secureIds = [
				...($tagIds === undefined ? [] : $tagIds),
				...($filterSelection ? $selectionIds : [])
			];
			const dataIds = [...new Set(secureIds)];
			sliceFinderReturn = await zenoClient.runSliceFinder($project.uuid, {
				metricColumn,
				searchColumns,
				orderBy: orderByOptions[orderByIdx],
				alpha: parseFloat(alphas[alphaIdx]),
				maxLattice: parseInt(maxlattice[maxlatticeIdx]),
				compareColumn,
				filterPredicates: $selectionPredicates,
				dataIds
			});
		}

		if (sliceFinderReturn.slices.length === 0) {
			sliceFinderMessage =
				'No slices found, try to increase alpha or add more search columns or predicates.';
		} else {
			sliceFinderMessage = '';
		}
	}

	function submit(e: KeyboardEvent) {
		if (e.key === 'Escape') {
			dispatch('close');
		}
	}
</script>

<svelte:window on:keydown={submit} />
<Popup on:close>
	<div class="flex items-center justify-between">
		<div class="flex items-center">
			<h3 class="mb-0 mt-0 pl-5 text-left">Slice Finder</h3>
			<div
				class="h-6 w-6 cursor-help fill-grey-dark"
				use:tooltip={{
					text: $page.url.href.includes('compare')
						? 'Run the SliceLine algorithm to find slices with the largest or smallest average difference in a difference column between two systems'
						: 'Run the SliceLine algorithm to find slices of data with high or low metrics'
				}}
			>
				<Icon tag="svg" viewBox="-6 -6 36 36">
					<path d={mdiInformationOutline} />
				</Icon>
			</div>
		</div>
		<IconButton on:click={() => dispatch('close')}>
			<Icon tag="svg" viewBox="0 0 24 24">
				<path d={mdiClose} />
			</Icon>
		</IconButton>
	</div>
	<div class="flex items-center">
		<div style:margin-left={'20px'}>
			<div class="flex">
				<div class="mb-2 mt-2">
					{$page.url.href.includes('compare') ? 'Difference Column' : 'Metric Column'}
				</div>
				<div
					class="mt-1 h-6 w-6 cursor-help fill-grey-dark"
					use:tooltip={{
						text: $page.url.href.includes('compare')
							? 'The column on which to measure system disagreement'
							: 'The continuous column to compare slices across'
					}}
				>
					<Icon tag="svg" viewBox="-6 -6 36 36">
						<path d={mdiInformationOutline} />
					</Icon>
				</div>
			</div>
			<Svelecte
				style="margin-right: 5px; width: 175px"
				bind:value={metricColumn}
				valueAsObject={true}
				valueField={'name'}
				labelField={'name'}
				options={metricColumns}
				placeholder="Metric Column"
			/>
		</div>
		<div style:width="100%">
			<div class="flex">
				<div class="mb-2 mt-2">Search Columns</div>
				<div
					class="mt-1 h-6 w-6 cursor-help fill-grey-dark"
					use:tooltip={{
						text: 'Metadata columns used to create slices'
					}}
				>
					<Icon tag="svg" viewBox="-6 -6 36 36">
						<path d={mdiInformationOutline} />
					</Icon>
				</div>
			</div>
			<Svelecte
				style="margin-right: 5px;"
				bind:value={searchColumns}
				valueField={'name'}
				labelField={'name'}
				valueAsObject={true}
				options={searchColumnOptions}
				multiple={true}
				placeholder="Slicing Columns"
			/>
		</div>
		<div>
			<div class="flex">
				<div class="mb-2 mt-2">Alpha</div>
				<div
					class="mt-1 h-6 w-6 cursor-help fill-grey-dark"
					use:tooltip={{
						text: 'Weight parameter for the average slice metric. Increase it to find more slices'
					}}
				>
					<Icon tag="svg" viewBox="-6 -6 36 36">
						<path d={mdiInformationOutline} />
					</Icon>
				</div>
			</div>
			<Svelecte
				style="margin-right: 5px; width: 80px"
				bind:value={alphaIdx}
				options={alphas}
				required={true}
				placeholder="Alpha"
			/>
		</div>
		<div>
			<div class="flex">
				<div class="mb-2 mt-2">Max. Lattice</div>
				<div
					class="mt-1 h-6 w-6 cursor-help fill-grey-dark"
					use:tooltip={{
						text: 'Maximum number of predicates'
					}}
				>
					<Icon tag="svg" viewBox="-6 -6 36 36">
						<path d={mdiInformationOutline} />
					</Icon>
				</div>
			</div>
			<Svelecte
				style="margin-right: 5px; width: 120px"
				bind:value={maxlatticeIdx}
				options={maxlattice}
				placeholder="Maximum lattice level"
			/>
		</div>
		<div>
			<div class="flex">
				<div class="mb-2 mt-2">Order By</div>
				<div
					class="mt-1 h-6 w-6 cursor-help fill-grey-dark"
					use:tooltip={{
						text: $page.url.href.includes('compare')
							? 'Order by slice score, a combination of system difference and size'
							: 'Order by slice score, a combination of size and metric'
					}}
				>
					<Icon tag="svg" viewBox="-6 -6 36 36">
						<path d={mdiInformationOutline} />
					</Icon>
				</div>
			</div>
			<Svelecte
				style="width: 150px; margin-right: 20px"
				bind:value={orderByIdx}
				options={$page.url.href.includes('compare') ? compareOrderByOptions : orderByOptions}
				renderer={svelecteRenderer}
				placeholder="Order By"
			/>
		</div>
	</div>
	{#if $selectionPredicates !== undefined || $selections.tags.length > 0}
		<div class="mx-5">
			<div class="mb-2 mt-2">Search for slices in:</div>
			<div class="flex rounded border border-grey-lighter">
				<ChipsWrapper />
			</div>
		</div>
	{/if}
	{#if sliceFinderReturn.slices.length > 0}
		<div class="m-5 flex items-center justify-between">
			<Button
				variant="raised"
				on:click={() => generateSlices()}
				on:mouseleave={blur}
				on:focusout={blur}
			>
				Generate Slices
			</Button>
			<span class="m-2.5">{sliceFinderMessage}</span>
			<div>
				<span class="mr-3"> Overall Average: </span>
				<span class="average-value text-primary">
					{sliceFinderReturn.overallMetric ? sliceFinderReturn.overallMetric.toFixed(2) : ''}
				</span>
			</div>
		</div>
		<div class="m-5 flex items-center justify-between">
			<h4>Filter Predicates</h4>
			<h4>
				Average Slice Metric {$page.url.href.includes('compare') ? 'difference' : ''}
			</h4>
		</div>
	{:else}
		<div class="m-5 flex flex-col items-center justify-center">
			<Button
				variant="raised"
				on:click={() => generateSlices()}
				on:mouseleave={blur}
				on:focusout={blur}
			>
				Generate Slices
			</Button>
			<span class="m-2.5 ml-5">
				Find slices with {$page.url.href.includes('compare')
					? 'the largest difference'
					: 'the lowest performance'}
			</span>
			<span class="m-2.5">{sliceFinderMessage}</span>
		</div>
	{/if}
	<div class="flex flex-col overflow-y-auto">
		{#each sliceFinderReturn.slices as slice, idx}
			{@const metric = sliceFinderReturn.metrics[idx].toFixed(2)}
			{@const size = sliceFinderReturn.sizes[idx]}
			<SliceFinderCell {slice} {metric} {size} />
		{/each}
	</div>
</Popup>
