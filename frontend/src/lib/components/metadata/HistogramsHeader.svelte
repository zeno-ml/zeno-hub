<script lang="ts">
	import MetricRange from '$lib/components/metadata/MetricRange.svelte';
	import { requestingHistogramCounts } from '$lib/stores';
	import { tooltip } from '$lib/util/tooltip';
	import { mdiInformationOutline } from '@mdi/js';
	import CircularProgress from '@smui/circular-progress';
	import { Icon } from '@smui/icon-button';
</script>

<div class="flex items-center justify-between py-3">
	<div class="flex items-center justify-between">
		<h4 class="text-grey-dark">Metadata</h4>
		<div
			class="h-6 w-6 cursor-help fill-grey-dark"
			use:tooltip={{
				text: 'Interactive distributions for metadata columns. Click or drag on the histograms to filter the data'
			}}
		>
			<Icon style="outline:none" tag="svg" viewBox="-6 -6 36 36">
				<path d={mdiInformationOutline} />
			</Icon>
		</div>
		{#if $requestingHistogramCounts}
			<CircularProgress style="height: 15px; width: 15px; margin-left: 10px;" indeterminate />
		{/if}
	</div>
	<MetricRange />
</div>
