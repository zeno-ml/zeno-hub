<script lang="ts">
	import { ReportElementType, type Chart, type ReportElement } from '$lib/zenoapi';
	import ChartElement from './ChartElement.svelte';
	import TextElement from './TextElement.svelte';

	export let element: ReportElement;
	export let chartOptions: Promise<Chart[]>;
</script>

<div class="flex items-center my-2">
	{#if element.type === ReportElementType.TEXT}
		<TextElement {element} />
	{:else if element.type === ReportElementType.CHART}
		{#await chartOptions then options}
			<ChartElement chart={options.filter((c) => c.id === element.chartId)[0]} />
		{/await}
	{/if}
</div>
