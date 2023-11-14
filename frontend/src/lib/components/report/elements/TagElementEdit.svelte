<script lang="ts">
	import { svelecteRenderer, svelecteRendererName } from '$lib/util/util';
	import type {
		ReportElement,
		Tag,
		SliceElementSpec as TagElementSpec,
		ZenoService
	} from '$lib/zenoapi';
	import Svelecte from 'svelecte';
	import { getContext } from 'svelte';

	export let element: ReportElement;
	export let tagOptions: Tag[];
	export let reportId: number;
	export let tagElementSpec: TagElementSpec;

	const zenoClient = getContext('zenoClient') as ZenoService;
	let models: string[] = [];

	$: projectUuid = tagOptions.find((sli) => sli.id === tagElementSpec.tagId)?.projectUuid ?? null;
	$: if (projectUuid !== null) {
		zenoClient.getModels(projectUuid).then((modelsRequest) => {
			models = modelsRequest;
		});
	}

	function updateTagId(e: CustomEvent) {
		tagElementSpec = {
			tagId: e.detail.id
		};
		let res = tagOptions.find((sli) =>
			sli.id === tagElementSpec?.tagId ? tagElementSpec.tagId : ''
		);
		if (res && res.projectUuid) {
			projectUuid = res.projectUuid;
		}

		element.data = JSON.stringify(tagElementSpec);
		zenoClient.updateReportElement(reportId, {
			...element,
			data: element.data
		});
	}

	function updateTagModel(e: CustomEvent) {
		tagElementSpec = {
			tagId: tagElementSpec.tagId,
			modelName: e.detail.label
		};
		element = { ...element, data: JSON.stringify(tagElementSpec) };
		zenoClient.updateReportElement(reportId, {
			...element,
			data: element.data
		});
	}
</script>

{#await zenoClient.getProjects() then projects}
	{@const options = tagOptions.map((s) => {
		return {
			name: `${s.tagName} (${projects.find((p) => p.uuid === s.projectUuid)?.name})`,
			id: s.id
		};
	})}
	<Svelecte
		value={tagElementSpec.tagId}
		{options}
		on:change={updateTagId}
		valueField="id"
		labelField="name"
		renderer={svelecteRendererName}
	/>
{/await}
{#if models.length > 0}
	<div class="mt-3" />
	<Svelecte
		bind:value={tagElementSpec.modelName}
		labelAsValue={true}
		options={models}
		on:change={updateTagModel}
		renderer={svelecteRenderer}
	/>
{/if}
