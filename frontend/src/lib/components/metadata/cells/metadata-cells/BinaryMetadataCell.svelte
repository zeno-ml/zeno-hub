<script lang="ts">
	import { Label } from '@smui/common';
	import { scaleLinear } from 'd3-scale';
	import { metricRangeColorScale } from '$lib/stores';
	import { Join, type FilterPredicate, type ZenoColumn, Operation } from '$lib/zenoapi';
	import type { HistogramEntry } from '$lib/api/metadata';

	export let col: ZenoColumn;
	export let histogram: HistogramEntry[];
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
		.domain([0, (histogram[0].filteredCount || 0) + (histogram[1].filteredCount || 0)])
		.range([20, 80]);

	$: selectedValue = filterPredicates.length > 0 ? filterPredicates[0].value : null;
</script>

{#if histogram}
	<div class="binary-button-wrapper">
		<div class="binary-button-single" style:width="{widthScale(histogram[0].filteredCount)}%">
			<div
				class="binary-button left {selectedValue !== null && selectedValue === true
					? 'selected'
					: ''}"
				style="color: white; background-color: {$metricRangeColorScale(histogram[0].metric || 0)}"
				on:click={() => setSelection(true)}
				on:keydown={() => setSelection(true)}
			>
				<Label>True</Label>
			</div>
			<small>{histogram[0].filteredCount} / {histogram[0].count}</small>
		</div>
		<div class="binary-button-single" style:width="{widthScale(histogram[1].filteredCount)}%">
			<div
				class="binary-button right {selectedValue !== null && selectedValue === false
					? 'selected'
					: ''}"
				style="color: white; background-color: {$metricRangeColorScale(histogram[1].metric || 0)}"
				on:click={() => setSelection(false)}
				on:keydown={() => setSelection(false)}
			>
				<Label>False</Label>
			</div>
			<small>{histogram[1].filteredCount} / {histogram[1].count}</small>
		</div>
	</div>
{/if}

<style>
	.binary-button {
		display: flex;
		padding: 5px 20px 5px 20px;
		cursor: pointer;
		flex-direction: column;
		align-items: center;
		box-sizing: border-box;
		border: 3px solid transparent;
		font-weight: 700;
	}
	.right {
		border-top-right-radius: 5px;
		border-bottom-right-radius: 5px;
	}
	.left {
		border-top-left-radius: 5px;
		border-bottom-left-radius: 5px;
	}
	.selected {
		box-sizing: border-box;
		border: 3px solid var(--P1);
	}
	.binary-button-wrapper {
		display: flex;
		padding-left: 5px;
		padding-right: 5px;
		width: 100%;
	}
	small {
		font-size: 12px;
	}
</style>
