<script lang="ts">
	import { ReportElementType, type Chart, type ReportElement } from '$lib/zenoapi';
	import ChartElement from './elements/ChartElement.svelte';
	import SliceElement from './elements/SliceElement.svelte';
	import TagElement from './elements/TagElement.svelte';
	import TextElement from './elements/TextElement.svelte';

	export let element: ReportElement;
	export let chartOptions: Chart[];

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
	<div class="my-2 ml-2 flex items-center" bind:clientWidth={width}>
		{#if element.type === ReportElementType.TEXT}
			<TextElement {element} />
		{:else if element.type === ReportElementType.CHART && chartOptions.length > 0}
			<ChartElement chart={chartOptions.filter((c) => c.id === chartId)[0]} {width} />
		{:else if element.type === ReportElementType.SLICE}
			<SliceElement {element} />
		{:else if element.type === ReportElementType.TAG}
			<TagElement {element} />
		{/if}
	</div>
{:else}
	<p>ERROR: Unable to load report element.</p>
{/if}
