<script lang="ts">
	import {
		ReportElementType,
		ZenoService,
		type Chart,
		type ReportElement,
		type Slice,
		type SliceElementSpec
	} from '$lib/zenoapi';
	import Svelecte from 'svelecte';
	import { getContext } from 'svelte';
	import ChartElementEdit from './elements/ChartElementEdit.svelte';
	import SliceElementEdit from './elements/SliceElementEdit.svelte';
	import TextElementEdit from './elements/TextElementEdit.svelte';

	export let element: ReportElement;
	export let chartOptions: Chart[];
	export let sliceOptions: Slice[];
	export let reportId: number;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let sliceElementSpec: SliceElementSpec | null =
		element.type === ReportElementType.SLICE ? JSON.parse(element.data as string) : null;

	// If there are no charts, then users should not be able to add a chart element
	$: elementOptions =
		chartOptions.length > 0
			? Object.values(ReportElementType)
			: Object.values(ReportElementType).filter((e) => e !== ReportElementType.CHART);

	async function updateType(e: CustomEvent) {
		let data = null;

		if (e.detail.label === ReportElementType.CHART) {
			const chartId = chartOptions[0].id;
			data = `${chartId}`;
		} else if (e.detail.label === ReportElementType.SLICE) {
			sliceElementSpec = { sliceId: sliceOptions[0].id, modelName: null };
			data = JSON.stringify(sliceElementSpec);
		}

		element = {
			...element,
			type: e.detail.label,
			data: data
		};
		await zenoClient.updateReportElement(reportId, element);
	}
</script>

<div class="flex p-3 h-full">
	<div class="flex flex-col w-full">
		<Svelecte
			style="margin-bottom: 10px;"
			value={element.type}
			labelAsValue={true}
			options={elementOptions}
			on:change={updateType}
		/>
		{#if element.type === ReportElementType.CHART}
			<ChartElementEdit bind:element {chartOptions} {reportId} />
		{:else if element.type === ReportElementType.TEXT}
			<TextElementEdit bind:element {reportId} />
		{:else if element.type === ReportElementType.SLICE && sliceElementSpec}
			<SliceElementEdit bind:element {sliceOptions} bind:sliceElementSpec {reportId} />
		{/if}
	</div>
</div>
