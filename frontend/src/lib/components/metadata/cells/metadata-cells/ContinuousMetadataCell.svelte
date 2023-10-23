<script lang="ts">
	import { metricRange } from '$lib/stores';
	import {
		Join,
		Operation,
		type FilterPredicate,
		type HistogramBucket,
		type ZenoColumn
	} from '$lib/zenoapi';
	import type { View } from 'svelte-vega';
	import { VegaLite } from 'svelte-vega';
	import { continuousVegaSpec } from './vegaSpecs';

	export let col: ZenoColumn;
	export let histogram: HistogramBucket[];
	export let filterPredicates: FilterPredicate[];
	export let updatePredicates: (predicates: FilterPredicate[]) => void;

	let view: View;
	let timer: ReturnType<typeof setTimeout>;

	$: if (view) {
		view.removeSignalListener('brush', setSelection);
		if (filterPredicates.length === 0) {
			view.signal('brush_x', []);
		}
		view.addSignalListener('brush', setSelection);
	}

	function setSelection(_: string, entry: Record<string, [number, number]>) {
		clearTimeout(timer);
		if (entry.bucket === undefined) {
			updatePredicates([]);
			return;
		}
		const data = entry.bucket;
		if (isNaN(data[0]) || isNaN(data[1])) {
			updatePredicates([]);
			return;
		}
		timer = setTimeout(() => {
			filterPredicates[0] = {
				column: col,
				operation: Operation.GTE,
				value: data[0],
				join: Join._
			} as FilterPredicate;
			filterPredicates[1] = {
				column: col,
				operation: Operation.LTE,
				value: data[1],
				join: Join.AND
			} as FilterPredicate;
			updatePredicates(filterPredicates);
		}, 100);
	}
</script>

<!-- We shallow copy histogram to remove the vega identifiers and force it to update the chart when new data is passed in. -->
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
