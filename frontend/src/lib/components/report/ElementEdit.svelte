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

	export let element: ReportElement;
	export let chartOptions: Promise<Chart[]>;
	export let sliceOptions: Promise<Slice[]>;
	export let reportId: number;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let timer: ReturnType<typeof setTimeout>;
	let projectUuid: string | null = null;
	let sliceElementSpec: SliceElementSpec | null = null;
	let chartId: number | null = null;
	let models: string[] = [];

	updateTypeObjects(element);

	// set specific objects for each element type from the raw data string.
	function updateTypeObjects(el: ReportElement) {
		if (el.type === ReportElementType.CHART) {
			if (el.data) {
				chartId = parseInt(el.data);
			} else {
				chartOptions.then((r) => (chartId = r[0].id));
			}
		} else if (el.type === ReportElementType.SLICE) {
			if (el.data) {
				sliceElementSpec = JSON.parse(el.data);
				sliceOptions.then((r) => {
					let res = r.find((sli) =>
						sli.id === sliceElementSpec?.sliceId ? sliceElementSpec.sliceId : ''
					);
					if (res && res.projectUuid) {
						projectUuid = res.projectUuid;
					}
				});
			} else {
				sliceOptions.then((r) => (sliceElementSpec = { sliceId: r[0].id, modelName: '' }));
			}
		}
	}

	$: if (projectUuid) {
		zenoClient.getModels(projectUuid).then((m) => (models = m));
	}

	function updateType(e: CustomEvent) {
		element.data = null;
		updateTypeObjects(element);
		element = element;
		zenoClient.updateReportElement(reportId, {
			...element,
			type: e.detail.label,
			data: null
		});
	}

	function updateData() {
		clearTimeout(timer);
		timer = setTimeout(() => {
			zenoClient.updateReportElement(reportId, element);
		}, 1000);
	}

	function updateChartId(e: CustomEvent) {
		element.data = `${e.detail.id}`;
		zenoClient.updateReportElement(reportId, { ...element, data: element.data });
	}

	function updateSliceId(e: CustomEvent) {
		if (!sliceElementSpec) return;
		sliceElementSpec = {
			sliceId: e.detail.id,
			modelName: sliceElementSpec.modelName
		};
		sliceOptions.then((r) => {
			let res = r.find((sli) =>
				sli.id === sliceElementSpec?.sliceId ? sliceElementSpec.sliceId : ''
			);
			if (res && res.projectUuid) {
				projectUuid = res.projectUuid;
			}
		});

		element.data = JSON.stringify(sliceElementSpec);
		zenoClient.updateReportElement(reportId, {
			...element,
			data: element.data
		});
	}

	function updateSliceModel(e: CustomEvent) {
		if (!sliceElementSpec) return;
		sliceElementSpec = {
			sliceId: sliceElementSpec.sliceId,
			modelName: e.detail.label
		};
		element.data = JSON.stringify(sliceElementSpec);
		zenoClient.updateReportElement(reportId, {
			...element,
			data: element.data
		});
	}
</script>

<div class="flex items-center p-3">
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
				<Svelecte value={chartId} {options} on:change={updateChartId} />
			{/await}
		{:else if element.type === ReportElementType.TEXT}
			<textarea
				class="h-44 border rounded border-grey-light p-2"
				on:input={updateData}
				bind:value={element.data}
				style="width: 100%;"
			/>
		{:else if element.type === ReportElementType.SLICE && sliceElementSpec}
			{#await sliceOptions then options}
				<Svelecte value={sliceElementSpec.sliceId} {options} on:change={updateSliceId} />
				{#if models.length > 0}
					<div class="mt-3" />
					<Svelecte
						bind:value={sliceElementSpec.modelName}
						labelAsValue={true}
						options={models}
						on:change={updateSliceModel}
					/>
				{/if}
			{/await}
		{/if}
	</div>
</div>
