<script lang="ts">
	import { ReportElementType, type Chart, type ReportElement } from '$lib/zenoapi';
	import ChartElement from './elements/ChartElement.svelte';
	import InstancesElement from './elements/InstancesElement.svelte';
	import TextElement from './elements/TextElement.svelte';

	export let element: ReportElement;
	export let chartOptions: Promise<Chart[]>;

	let width;
</script>

<div class="flex items-center my-2" bind:clientWidth={width}>
	{#if element.type === ReportElementType.TEXT}
		<TextElement {element} />
	{:else if element.type === ReportElementType.CHART}
		{#await chartOptions then options}
			<ChartElement
				chart={options.filter((c) => c.id === element.chartId)[0]}
				width={width - 200}
			/>
		{/await}
	{:else if element.type === ReportElementType.INSTANCES}
		<InstancesElement {element} />
	{/if}
</div>
