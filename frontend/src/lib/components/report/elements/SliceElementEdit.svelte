<script lang="ts">
	import { svelecteRenderer, svelecteRendererName } from '$lib/util/util';
	import type { ReportElement, Slice, SliceElementSpec, ZenoService } from '$lib/zenoapi';
	import Svelecte from 'svelecte';
	import { getContext } from 'svelte';

	export let element: ReportElement;
	export let sliceOptions: Slice[];
	export let reportId: number;
	export let sliceElementSpec: SliceElementSpec;

	const zenoClient = getContext('zenoClient') as ZenoService;
	let models: string[] = [];

	$: projectUuid =
		sliceOptions.find((sli) => sli.id === sliceElementSpec.sliceId)?.projectUuid ?? null;
	$: if (projectUuid !== null) {
		zenoClient.getModels(projectUuid).then((modelsRequest) => {
			models = modelsRequest;
		});
	}

	function updateSliceId(e: CustomEvent) {
		sliceElementSpec = {
			sliceId: e.detail.id
		};
		let res = sliceOptions.find((sli) =>
			sli.id === sliceElementSpec?.sliceId ? sliceElementSpec.sliceId : ''
		);
		if (res && res.projectUuid) {
			projectUuid = res.projectUuid;
		}

		element.data = JSON.stringify(sliceElementSpec);
		zenoClient.updateReportElement(reportId, {
			...element,
			data: element.data
		});
	}

	function updateSliceModel(e: CustomEvent) {
		sliceElementSpec = {
			sliceId: sliceElementSpec.sliceId,
			systemName: e.detail.label
		};
		element = { ...element, data: JSON.stringify(sliceElementSpec) };
		zenoClient.updateReportElement(reportId, {
			...element,
			data: element.data
		});
	}
</script>

{#await zenoClient.getUserProjects() then projects}
	{@const options = sliceOptions.map((s) => {
		return {
			name: `${s.sliceName} (${projects.find((p) => p.uuid === s.projectUuid)?.name})`,
			id: s.id
		};
	})}
	<Svelecte
		value={sliceElementSpec.sliceId}
		{options}
		on:change={updateSliceId}
		valueField="id"
		labelField="name"
		renderer={svelecteRendererName}
	/>
{/await}
{#if models.length > 0}
	<div class="mt-3" />
	<Svelecte
		bind:value={sliceElementSpec.systemName}
		labelAsValue={true}
		options={models}
		on:change={updateSliceModel}
		renderer={svelecteRenderer}
	/>
{/if}
