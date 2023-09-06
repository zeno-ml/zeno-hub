<script lang="ts">
	import InstanceView from '$lib/components/instance-views/InstanceView.svelte';
	import {
		compareSort,
		comparisonColumn,
		comparisonModel,
		metric,
		metricRange,
		model,
		selections
	} from '$lib/stores.js';
	import { setURLParameters } from '$lib/util/util.js';

	export let data;

	model.subscribe(() => setURLParameters());
	metric.subscribe(() => setURLParameters());
	comparisonModel.subscribe(() => setURLParameters());
	comparisonColumn.subscribe(() => setURLParameters());
	compareSort.subscribe(() => setURLParameters());
	metricRange.subscribe(() => setURLParameters());
	selections.subscribe(() => setURLParameters());
</script>

<div class="mx-5 flex flex-col flex-grow w-1">
	<InstanceView compare={data.compare} />
</div>
