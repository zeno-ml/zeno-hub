<script lang="ts">
	import { ReportElementType, ZenoService, type Chart, type ReportElement } from '$lib/zenoapi';
	import { mdiClose, mdiDrag } from '@mdi/js';
	import { Icon } from '@smui/button';
	import IconButton from '@smui/icon-button';
	import Svelecte from 'svelecte';
	import { createEventDispatcher } from 'svelte';

	export let element: ReportElement;
	export let chartOptions: Promise<Chart[]>;
	export let dragEnabled = false;
	export let reportId: number;

	let timer: ReturnType<typeof setTimeout>;

	const dispatch = createEventDispatcher();

	function updateType(e: CustomEvent) {
		ZenoService.updateReportElement(reportId, { ...element, type: e.detail.label });
	}

	function updateData() {
		clearTimeout(timer);
		timer = setTimeout(() => {
			ZenoService.updateReportElement(reportId, element);
		}, 1000);
	}

	function updateChart(e: CustomEvent) {
		ZenoService.updateReportElement(reportId, { ...element, chartId: e.detail.id });
	}
</script>

<div class="flex items-center my-2 border border-grey-light rounded p-4">
	<div class="flex mr-2 cursor-move">
		<Icon
			style="outline:none; width: 24px; height: 24px"
			tag="svg"
			viewBox="0 0 24 24"
			on:mousedown={() => (dragEnabled = true)}
		>
			<path fill="black" d={mdiDrag} />
		</Icon>
	</div>
	<div class="w-full">
		<Svelecte
			style="margin-bottom: 10px;"
			bind:value={element.type}
			labelAsValue={true}
			options={[ReportElementType.CHART, ReportElementType.TEXT]}
			on:change={updateType}
		/>
		{#if element.type === ReportElementType.CHART}
			{#await chartOptions then options}
				<Svelecte bind:value={element.chartId} {options} on:change={updateChart} />
			{/await}
		{:else if element.type === ReportElementType.TEXT}
			<textarea
				class="h-44 border rounded border-grey-light p-2"
				on:input={updateData}
				bind:value={element.data}
				style="width: 100%;"
			/>
		{/if}
	</div>
	<div class="flex">
		<IconButton on:click={() => dispatch('delete')}>
			<Icon tag="svg" viewBox="0 0 24 24">
				<path fill="black" d={mdiClose} />
			</Icon>
		</IconButton>
	</div>
</div>
