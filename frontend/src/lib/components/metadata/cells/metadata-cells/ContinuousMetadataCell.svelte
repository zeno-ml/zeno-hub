<script lang="ts">
	import type { HistogramEntry } from '$lib/api/metadata';
	import { metricRange } from '$lib/stores';
	import { Join, Operation, type FilterPredicate, type ZenoColumn } from '$lib/zenoapi';
	import type { View } from 'svelte-vega';
	import { VegaLite } from 'svelte-vega';
	import { continuousVegaSpec } from './vegaSpecs';

	export let col: ZenoColumn;
	export let histogram: HistogramEntry[];
	export let filterPredicates: FilterPredicate[];
	export let updatePredicates: (predicates: FilterPredicate[]) => void;

	let view: View;
	let localSelection = [];
	let localSelectionX = [];

	function updateSel() {
		if (filterPredicates.length !== 0) {
			view.signal('brush', { bucket: localSelection });
			view.signal('brush_x', localSelectionX);
		} else {
			view.signal('brush', {});
			view.signal('brush_x', []);
		}
		view.runAsync();
	}

	$: if (view && filterPredicates) {
		updateSel();
	}

	$: if (view) {
		view.addSignalListener('brush', (...s) => (localSelection = s[1].bucket ? s[1].bucket : []));
		view.addSignalListener('brush_x', (...s) => (localSelectionX = s[1]));
	}

	function setSelection() {
		if (localSelection.length > 0) {
			filterPredicates[0] = {
				column: col,
				operation: Operation.GTE,
				value: localSelection[0],
				join: Join._
			} as FilterPredicate;
			filterPredicates[1] = {
				column: col,
				operation: Operation.LTE,
				value: localSelection[1],
				join: Join.AND
			} as FilterPredicate;
		} else {
			localSelection = [];
			filterPredicates = [];
		}
		updatePredicates(filterPredicates);
	}
</script>

<!-- We shallow copy histogram to remove the vega identifiers and force it to update the chart when new data is passed in. -->
<div id="histogram" on:mouseup={setSelection}>
	<VegaLite
		bind:view
		spec={continuousVegaSpec($metricRange)}
		data={{ table: histogram.map((h) => Object.assign({}, h)) }}
		options={{
			tooltip: true,
			actions: false,
			theme: 'vox',
			renderer: 'svg'
		}}
	/>
</div>
