<script lang="ts">
	import { doesModelDependOnPredicates, getMetricsForSlices } from '$lib/api/slice';
	import { metric, selections } from '$lib/stores';
	import type { Slice } from '$lib/zenoapi';

	export let compare: boolean;
	export let slice: Slice;
	export let sliceModel: string;

	$: compareButton = doesModelDependOnPredicates(slice.filterPredicates.predicates);
	$: selected = $selections.slices.includes(slice.id);
	$: compareButtonstyle = compareButton
		? 'border border-grey-lighter hover:cursor-pointer ' + (selected ? 'bg-primary-light' : '')
		: '';
</script>

{#await getMetricsForSlices( [{ slice: slice, model: sliceModel, metric: $metric ? $metric.id : -1 }] ) then res}
	{#if res !== null}
		<div
			class={compare
				? 'flex flex-col items-center mr-2.5 p text-xs ' + compareButtonstyle
				: 'flex items-center'}
			on:keydown={() => ({})}
		>
			<span class="mr-2 text-right">
				{res[0].metric !== undefined && res[0].metric !== null ? res[0].metric.toFixed(2) : ''}
			</span>
			<span class="mr-1 text-right italic text-grey-dark">
				({res[0].size.toLocaleString()})
			</span>
		</div>
	{/if}
{/await}
