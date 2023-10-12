<script lang="ts">
	import { page } from '$app/stores';
	import {
		columns,
		comparisonModel,
		model,
		project,
		selectionIds,
		selectionPredicates,
		selections,
		tagIds
	} from '$lib/stores';
	import { columnSort } from '$lib/util/util';
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
	import { tooltip } from '@svelte-plugins/tooltips';
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
			const secureTagIds = $tagIds === undefined ? [] : $tagIds;
			const secureSelectionIds = $selectionIds === undefined ? [] : $selectionIds;
			const dataIds = [...new Set([...secureTagIds, ...secureSelectionIds])];
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
			<h3 class="text-left pl-5 mb-0 mt-0">Slice Finder</h3>
			<div
				class="w-6 h-6 cursor-help fill-grey-dark"
				use:tooltip={{
					content: $page.url.href.includes('compare')
						? 'Run the SliceLine algorithm to find slices with the largest or smallest average difference in a difference column between two systems'
						: 'Run the SliceLine algorithm to find slices of data with high or low metrics',
					position: 'right',
					theme: 'zeno-tooltip',
					maxWidth: '350'
				}}
			>
				<Icon style="outline:none" tag="svg" viewBox="-6 -6 36 36">
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
			<div style="display:flex">
				<div class="mt-2 mb-2">
					{$page.url.href.includes('compare') ? 'Difference Column' : 'Metric Column'}
				</div>
				<div
					class="w-6 h-6 cursor-help fill-grey-dark"
					style="margin-top: 3px;"
					use:tooltip={{
						content: $page.url.href.includes('compare')
							? 'The column on which to measure system disagreement'
							: 'The continuous column to compare slices across',
						position: 'right',
						theme: 'zeno-tooltip',
						maxWidth: '450'
					}}
				>
					<Icon style="outline:none" tag="svg" viewBox="-6 -6 36 36">
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
			<div style="display:flex">
				<div class="mb-2 mt-2">Search Columns</div>
				<div
					class="w-6 h-6 cursor-help fill-grey-dark"
					style="margin-top: 3px;"
					use:tooltip={{
						content: 'Metadata columns used to create slices',
						position: 'top',
						theme: 'zeno-tooltip',
						maxWidth: '450'
					}}
				>
					<Icon style="outline:none" tag="svg" viewBox="-6 -6 36 36">
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
			<div style="display:flex">
				<div class="mb-2 mt-2">Alpha</div>
				<div
					class="w-6 h-6 cursor-help fill-grey-dark"
					style="margin-top: 3px;"
					use:tooltip={{
						content:
							'Weight parameter for the average slice metric. Increase it to find more slices',
						theme: 'zeno-tooltip',
						maxWidth: '195',
						position: 'left'
					}}
				>
					<Icon style="outline:none" tag="svg" viewBox="-6 -6 36 36">
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
			<div style="display:flex">
				<div class="mb-2 mt-2">Max. Lattice</div>
				<div
					class="w-6 h-6 cursor-help fill-grey-dark"
					style="margin-top: 3px;"
					use:tooltip={{
						content: 'Maximum number of predicates',
						theme: 'zeno-tooltip',
						maxWidth: '270'
					}}
				>
					<Icon style="outline:none" tag="svg" viewBox="-6 -6 36 36">
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
			<div style="display:flex">
				<div class="mb-2 mt-2">Order By</div>
				<div
					class="w-6 h-6 cursor-help fill-grey-dark"
					style="margin-top: 3px;"
					use:tooltip={{
						content: $page.url.href.includes('compare')
							? 'Order by slice score, a combination of system difference and size'
							: 'Order by slice score, a combination of size and metric',
						theme: 'zeno-tooltip',
						position: 'left',
						maxWidth: '250'
					}}
				>
					<Icon style="outline:none" tag="svg" viewBox="-6 -6 36 36">
						<path d={mdiInformationOutline} />
					</Icon>
				</div>
			</div>
			<Svelecte
				style="width: 120px; margin-right: 20px"
				bind:value={orderByIdx}
				options={$page.url.href.includes('compare')
					? ['(system) A > B', '(system) B > A']
					: orderByOptions}
				placeholder="Order By"
			/>
		</div>
	</div>
	{#if $selectionPredicates !== undefined || $selections.tags.length > 0 || $selectionIds !== undefined}
		<div style="margin-left: 20px;margin-right: 20px">
			<div class="mb-2 mt-2">Search for slices in:</div>
			<div class="flex border border-grey-lighter rounded">
				<ChipsWrapper />
			</div>
		</div>
	{/if}
	{#if sliceFinderReturn.slices.length > 0}
		<div class="flex justify-between items-center m-5">
			<Button
				variant="outlined"
				style="color:white; background-color: var(--logo);"
				on:click={() => generateSlices()}
				on:mouseleave={blur}
				on:focusout={blur}
			>
				Generate Slices
			</Button>
			<span class="m-2.5">{sliceFinderMessage}</span>
			<div>
				<span class="mr-3"> Overall Average: </span>
				<span class="average-value" style="color: var(--logo);">
					{sliceFinderReturn.overallMetric ? sliceFinderReturn.overallMetric.toFixed(2) : ''}
				</span>
			</div>
		</div>
		<div class="flex justify-between items-center m-5" style="margin-bottom:0px;">
			<h4 style="margin-bottom:0px;">Filter Predicates</h4>
			<h4 style="margin-bottom:0px;">
				Average Slice Metric {$page.url.href.includes('compare') ? 'difference' : ''}
			</h4>
		</div>
	{:else}
		<div class="flex flex-col items-center justify-center m-5">
			<Button
				variant="outlined"
				style="color:white; background-color: var(--logo);"
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
