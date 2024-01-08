<script lang="ts">
	import { selections } from '$lib/stores';
	import {
		Join,
		MetadataType,
		type FilterPredicate,
		type FilterPredicateGroup,
		type HistogramBucket,
		type ZenoColumn
	} from '$lib/zenoapi';
	import BinaryMetadataCell from './metadata-cells/BinaryMetadataCell.svelte';
	import ContinuousMetadataCell from './metadata-cells/ContinuousMetadataCell.svelte';
	import NominalMetadataCell from './metadata-cells/NominalMetadataCell.svelte';
	import TextMetadataCell from './metadata-cells/TextMetadataCell.svelte';

	export let col: ZenoColumn;
	export let histogram: HistogramBucket[] | undefined;

	const columnMap = {
		[MetadataType.NOMINAL]: NominalMetadataCell,
		[MetadataType.CONTINUOUS]: ContinuousMetadataCell,
		[MetadataType.BOOLEAN]: BinaryMetadataCell,
		[MetadataType.DATETIME]: TextMetadataCell,
		[MetadataType.EMBEDDING]: TextMetadataCell,
		[MetadataType.OTHER]: TextMetadataCell
	};

	let filterPredicates: FilterPredicateGroup;
	$: filterPredicates = $selections.metadata[col.id]
		? $selections.metadata[col.id]
		: { predicates: [], join: Join._ };
	let predicates: FilterPredicate[] = [];
	$: predicates = filterPredicates.predicates as FilterPredicate[];

	function updatePredicates(predicates: FilterPredicate[]) {
		let metadata = {
			...$selections.metadata,
			[col.id]: { predicates, join: Join._ }
		};
		metadata = Object.keys(metadata)
			.filter((k) => metadata[k].predicates.length > 0)
			.reduce(
				(res, k) => ((res[k] = metadata[k]), res),
				{} as Record<string, FilterPredicateGroup>
			);
		selections.update((sel) => ({ ...sel, metadata: metadata }));
	}

	function getChartType(dataType: MetadataType, histogram: HistogramBucket[]) {
		if (dataType === MetadataType.NOMINAL && histogram.length == 0) {
			return columnMap[MetadataType.OTHER];
		} else {
			return columnMap[dataType];
		}
	}
</script>

<div class="flex flex-col border-b border-grey-lighter pb-2 pt-2">
	<div class="mb-2.5 ml-1 flex items-center justify-between text-grey-darker">
		<div class="label top-text">
			{col.name}
		</div>
	</div>
	{#if histogram}
		<svelte:component
			this={getChartType(col.dataType, histogram)}
			filterPredicates={predicates}
			{updatePredicates}
			{col}
			{histogram}
		/>
	{/if}
</div>
