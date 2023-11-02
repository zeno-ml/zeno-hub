<script lang="ts">
	import { metricRangeColorScale } from '$lib/stores';
	import {
		Join,
		Operation,
		type FilterPredicate,
		type HistogramBucket,
		type ZenoColumn
	} from '$lib/zenoapi';
	import { Label } from '@smui/common';
	import { scaleLinear } from 'd3-scale';

	export let col: ZenoColumn;
	export let histogram: HistogramBucket[];
	export let filterPredicates: FilterPredicate[];
	export let updatePredicates: (predicates: FilterPredicate[]) => void;

	function setSelection(setting: boolean) {
		if (filterPredicates.length === 0) {
			filterPredicates = [
				{
					column: col,
					operation: Operation.EQUAL,
					value: setting,
					join: Join._
				}
			];
		} else if (filterPredicates[0].value === setting) {
			filterPredicates = [];
		} else if (filterPredicates[0].value === true) {
			filterPredicates[0].value = false;
		} else {
			filterPredicates[0].value = true;
		}
		updatePredicates(filterPredicates);
	}

	$: widthScale = scaleLinear()
		.domain([0, (histogram[0].filteredSize ?? 0) + (histogram[1].filteredSize ?? 0)])
		.range([20, 80]);

	$: selectedValue = filterPredicates.length > 0 ? filterPredicates[0].value : null;
</script>

{#if histogram}
	<div class="flex w-full px-1">
		<div style:width="{widthScale(histogram[0].filteredSize ?? 0)}%">
			<button
				class="border-transparent box-border flex w-full cursor-pointer flex-col items-center rounded-l-xl border-2 px-1 py-2.5 font-bold text-background {selectedValue !==
					null && selectedValue === true
					? 'border-primary-mid'
					: 'border-yellowish-light'}"
				style="background-color: {$metricRangeColorScale(histogram[0].metric ?? 0)}"
				on:click={() => setSelection(true)}
				on:keydown={() => setSelection(true)}
			>
				<Label>True</Label>
			</button>
			<span class="text-xs">{histogram[0].filteredSize} / {histogram[0].size}</span>
		</div>
		<div style:width="{widthScale(histogram[1].filteredSize ?? 0)}%">
			<button
				class="border-transparent box-border flex w-full cursor-pointer flex-col items-center rounded-r-xl border-2 px-1 py-2.5 font-bold text-background {selectedValue !==
					null && selectedValue === false
					? 'border-primary-mid'
					: 'border-yellowish-light'}"
				style="background-color: {$metricRangeColorScale(histogram[1].metric ?? 0)}"
				on:click={() => setSelection(false)}
				on:keydown={() => setSelection(false)}
			>
				<Label>False</Label>
			</button>
			<span class="text-xs">{histogram[1].filteredSize} / {histogram[1].size}</span>
		</div>
	</div>
{/if}
