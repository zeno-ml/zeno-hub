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
	export let histogram: HistogramBucket[];

	const columnMap = {
		[MetadataType.NOMINAL]: NominalMetadataCell,
		[MetadataType.CONTINUOUS]: ContinuousMetadataCell,
		[MetadataType.BOOLEAN]: BinaryMetadataCell,
		[MetadataType.DATETIME]: TextMetadataCell,
		[MetadataType.OTHER]: TextMetadataCell
	};

	let filterPredicates: FilterPredicateGroup;
	$: filterPredicates = $selections.metadata[col.id]
		? $selections.metadata[col.id]
		: { predicates: [], join: Join._ };
	let predicates: FilterPredicate[] = [];
	$: predicates = filterPredicates.predicates as FilterPredicate[];

	function updatePredicates(predicates: FilterPredicate[]) {
		selections.update((mets) => ({
			slices: mets.slices,
			metadata: {
				...mets.metadata,
				[col.id]: { predicates, join: Join._ }
			},
			tags: mets.tags
		}));
	}

	function getChartType(dataType: MetadataType, histogram: HistogramBucket[]) {
		if (dataType === MetadataType.NOMINAL && histogram.length == 0) {
			return columnMap[MetadataType.OTHER];
		} else {
			return columnMap[dataType];
		}
	}
</script>

{#if histogram}
	<div class="border-b border-grey-lighter pb-2 pt-2 flex flex-col">
		<div class="flex justify-between items-center ml-1 mb-2.5 text-grey-darker">
			<div class="label top-text">
				<span>
					{col.name}
				</span>
			</div>
		</div>
		<svelte:component
			this={getChartType(col.dataType, histogram)}
			filterPredicates={predicates}
			{updatePredicates}
			{col}
			{histogram}
		/>
	</div>
{/if}
