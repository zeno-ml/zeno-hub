<script lang="ts">
	import {
		ReportElementType,
		ZenoService,
		type Chart,
		type ReportElement,
		type Slice,
		type SliceElementSpec
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

	const dispatch = createEventDispatcher();
	let timer: ReturnType<typeof setTimeout>;
	let projectUuid: string | undefined | null;
	let sliceElementSpec: SliceElementSpec;
	let models: string[] = [];

	$: if (projectUuid) {
		ZenoService.getModels(projectUuid).then((m) => {
			models = m;
			updateSliceModel(models[0]);
		});
	}

	if (element.data !== null && element.data !== undefined) {
		try {
			sliceElementSpec = JSON.parse(element.data);
			sliceOptions.then((r) => {
				projectUuid = r.find((sli) =>
					sli.id === sliceElementSpec?.sliceId ? sliceElementSpec.sliceId : ''
				)?.projectUuid;
			});
		} catch {
			sliceElementSpec = { sliceId: 0, modelName: '' };
		}
	}

	function updateType(e: CustomEvent) {
		ZenoService.updateReportElement(reportId, { ...element, type: e.detail.label });
	}

	function updateData() {
		clearTimeout(timer);
		timer = setTimeout(() => {
			ZenoService.updateReportElement(reportId, element);
		}, 1000);
	}

	function updateChartId(e: CustomEvent) {
		ZenoService.updateReportElement(reportId, { ...element, data: `${e.detail.id}` });
	}

	function updateSliceId(e: CustomEvent) {
		sliceElementSpec = {
			sliceId: e.detail.id,
			modelName: sliceElementSpec?.modelName
		};
		sliceOptions.then((r) => {
			projectUuid = r.find((sli) =>
				sli.id === sliceElementSpec?.sliceId ? sliceElementSpec.sliceId : ''
			)?.projectUuid;
		});

		element.data = JSON.stringify(sliceElementSpec);
		ZenoService.updateReportElement(reportId, {
			...element,
			data: element.data
		});
	}

	function updateSliceModelEvent(e: CustomEvent) {
		updateSliceModel(e.detail.label);
	}

	function updateSliceModel(model: string) {
		sliceElementSpec = {
			sliceId: sliceElementSpec?.sliceId,
			modelName: model
		};
		element.data = JSON.stringify(sliceElementSpec);
		ZenoService.updateReportElement(reportId, {
			...element,
			data: element.data
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
			options={Object.values(ReportElementType)}
			on:change={updateType}
		/>
		{#if element.type === ReportElementType.CHART}
			{#await chartOptions then options}
				<Svelecte bind:value={element.data} {options} on:change={updateChartId} />
			{/await}
		{:else if element.type === ReportElementType.TEXT}
			<textarea
				class="h-44 border rounded border-grey-light p-2"
				on:input={updateData}
				bind:value={element.data}
				style="width: 100%;"
			/>
		{:else if element.type === ReportElementType.SLICE}
			{#await sliceOptions then options}
				<Svelecte value={sliceElementSpec.sliceId} {options} on:change={updateSliceId} />
				{#if models.length > 0}
					<Svelecte
						labelAsValue={true}
						value={models[0]}
						options={models}
						on:change={updateSliceModelEvent}
					/>
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
