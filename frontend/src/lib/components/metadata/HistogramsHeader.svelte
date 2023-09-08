<script lang="ts">
	import MetricRange from '$lib/components/metadata/MetricRange.svelte';
	import { requestingHistogramCounts } from '$lib/stores';
	import { mdiInformationOutline } from '@mdi/js';
	import CircularProgress from '@smui/circular-progress';
	import { Icon } from '@smui/icon-button';
	import { tooltip } from '@svelte-plugins/tooltips';
</script>

<div
	class="flex items-center justify-between pt-2.5 top-24 border-b border-grey-lighter bg-yellowish-light z-10 pb-4"
>
	<div class="flex items-center justify-between">
		<h4>Metadata</h4>
		<div
			class="w-6 h-6 cursor-help fill-grey-dark"
			use:tooltip={{
				content:
					'Interactive distributions for metadata columns. Click or drag on the histograms to filter the data',
				position: 'right',
				theme: 'zeno-tooltip'
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
