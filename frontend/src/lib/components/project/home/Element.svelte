<script lang="ts">
	import Spinner from '$lib/components/general/Spinner.svelte';
	import { project } from '$lib/stores';
	import { ProjectHomeElementType, type ProjectHomeElement, type ZenoService } from '$lib/zenoapi';
	import { getContext } from 'svelte';
	import ChartElement from './elements/ChartElement.svelte';
	import ListElement from './elements/ListElement.svelte';

	export let element: ProjectHomeElement;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let width;
	let height;

	console.log(element);
	let chartId = -1;
	$: if (
		element.type === ProjectHomeElementType.CHART &&
		element.data !== null &&
		element.data !== undefined
	) {
		chartId = parseInt(element.data);
	}
</script>

<div
	class="relative flex h-full w-full flex-col overflow-hidden p-3"
	bind:clientWidth={width}
	bind:clientHeight={height}
>
	{#if element.type === ProjectHomeElementType.CHART}
		{#await zenoClient.getChart(chartId, $project.uuid)}
			<div class="flex h-full w-full items-center justify-center">
				<Spinner />
			</div>
		{:then chart}
			<ChartElement {chart} {width} {height} />
		{/await}
	{:else if element.type === ProjectHomeElementType.LIST}
		<ListElement />
	{/if}
</div>
