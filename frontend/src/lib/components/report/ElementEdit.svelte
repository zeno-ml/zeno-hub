<script lang="ts">
	import {
		ReportElementType,
		ZenoService,
		type Chart,
		type InstancesElement,
		type ReportElement,
		type Slice
	} from '$lib/zenoapi';
	import { mdiClose, mdiDrag } from '@mdi/js';
	import { Icon } from '@smui/button';
	import IconButton from '@smui/icon-button';
	import Svelecte from 'svelecte';
	import { createEventDispatcher } from 'svelte';

	export let element: ReportElement;
	export let chartOptions: Promise<Chart[]>;
	export let sliceOptions: Promise<Slice[]>;
	export let dragEnabled = false;
	export let reportId: number;

	let timer: ReturnType<typeof setTimeout>;
	let projectUuid: string | undefined | null;
	let instancesElementSpec: InstancesElement;

	if (element.data !== null && element.data !== undefined) {
		try {
			instancesElementSpec = JSON.parse(element.data);
			sliceOptions.then((r) => {
				projectUuid = r.find((sli) =>
					sli.id === instancesElementSpec?.sliceId ? instancesElementSpec.sliceId : ''
				)?.projectUuid;
			});
		} catch {
			instancesElementSpec = { sliceId: 0, modelName: '' };
		}
	}

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

	function updateInstancesSlice(e: CustomEvent) {
		instancesElementSpec = {
			sliceId: e.detail.id,
			modelName: instancesElementSpec?.modelName
		};
		sliceOptions.then((r) => {
			projectUuid = r.find((sli) =>
				sli.id === instancesElementSpec?.sliceId ? instancesElementSpec.sliceId : ''
			)?.projectUuid;
		});

		ZenoService.updateReportElement(reportId, {
			...element,
			data: JSON.stringify(instancesElementSpec)
		});
	}
	function updateInstancesModel(e: CustomEvent) {
		instancesElementSpec = {
			sliceId: instancesElementSpec?.sliceId,
			modelName: e.detail.label
		};
		ZenoService.updateReportElement(reportId, {
			...element,
			data: JSON.stringify(instancesElementSpec)
		});
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
			options={[ReportElementType.CHART, ReportElementType.TEXT, ReportElementType.INSTANCES]}
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
		{:else if element.type === ReportElementType.INSTANCES}
			{#await sliceOptions then options}
				<Svelecte value={instancesElementSpec.sliceId} {options} on:change={updateInstancesSlice} />
				{#if projectUuid}
					{#await ZenoService.getModels(projectUuid) then models}
						<Svelecte
							labelAsValue={true}
							value={models[0]}
							options={models}
							on:change={updateInstancesModel}
						/>
					{/await}
				{/if}
			{/await}
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
