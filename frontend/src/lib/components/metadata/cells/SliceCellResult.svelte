<script lang="ts">
	import {
		doesModelDependOnPredicates,
		getMetricsForSlices,
		setModelForFilterPredicateGroup
	} from '$lib/api/slice';
	import { metric, selections } from '$lib/stores';
	import type { Slice } from '$lib/zenoapi';
	import { selectModelDependSliceCell } from './sliceCellUtil';

	export let compare: boolean;
	export let slice: Slice;
	export let sliceModel: string;

	$: compareButton = doesModelDependOnPredicates(slice.filterPredicates.predicates);
	$: selected = $selections.slices.includes(slice.id);
	$: compareButtonstyle = compareButton
		? 'border border-grey-lighter hover:cursor-pointer pl-1 pr-1 pt-0.5 pb-0.5 ' +
		  (selected ? 'bg-primary-light' : '')
		: '';
</script>

{#await getMetricsForSlices( [{ slice: slice, model: sliceModel, metric: $metric ? $metric.id : -1 }] ) then res}
	{#if res !== null}
		<button
			class={compare
				? 'flex flex-col items-center mr-2.5 text-xs ' + compareButtonstyle
				: 'flex items-center'}
			on:click={(e) => {
				if (compare && compareButton) {
					e.stopPropagation();
					slice.filterPredicates = setModelForFilterPredicateGroup(
						slice.filterPredicates,
						sliceModel
					);
					selectModelDependSliceCell(slice);
				}
			}}
		>
			<span class="mr-2 text-right">
				{res[0].metric !== undefined && res[0].metric !== null ? res[0].metric.toFixed(2) : ''}
			</span>
			<span class="mr-1 text-right italic text-grey-dark">
				({res[0].size.toLocaleString()})
			</span>
		</button>
	{/if}
{/await}
