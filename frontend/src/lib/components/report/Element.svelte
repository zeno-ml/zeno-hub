<script lang="ts">
	import { ReportElementType, type Chart, type ReportElement } from '$lib/zenoapi';
	import ChartElement from './elements/ChartElement.svelte';
	import SliceElement from './elements/SliceElement.svelte';
	import TextElement from './elements/TextElement.svelte';

	export let element: ReportElement;
	export let chartOptions: Promise<Chart[]>;

	let width;

	let chartId = -1;
	$: if (
		element.type === ReportElementType.CHART &&
		element.data !== null &&
		element.data !== undefined
	) {
		chartId = parseInt(element.data);
	}
</script>

{#if element.data !== null && element.data !== undefined}
	<div class="flex items-center my-2 ml-2" bind:clientWidth={width}>
		{#if element.type === ReportElementType.TEXT}
			<TextElement {element} />
		{:else if element.type === ReportElementType.CHART}
			{#await chartOptions then options}
				<ChartElement chart={options.filter((c) => c.id === chartId)[0]} {width} />
			{/await}
		{:else if element.type === ReportElementType.SLICE}
			<SliceElement {element} />
		{/if}
	</div>
{/if}
