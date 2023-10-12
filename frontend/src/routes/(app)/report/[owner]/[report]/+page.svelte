<script lang="ts">
	import { goto } from '$app/navigation';
	import Element from '$lib/components/report/Element.svelte';
	import ElementEdit from '$lib/components/report/ElementEdit.svelte';
	import {
		ReportElementType,
		ZenoService,
		type Chart,
		type Project,
		type ReportElement,
		type Slice
	} from '$lib/zenoapi';
	import Button, { Label } from '@smui/button';
	import Svelecte from 'svelecte';
	import { getContext } from 'svelte';
	import { dndzone } from 'svelte-dnd-action';

	export let data;

	let elements = data.reportElements.sort((a, b) => a.position - b.position);
	let selectedProjects = data.report.linkedProjects ?? [];
	let isEdit = false;
	let dragEnabled = false;
	let chartOptions: Promise<Chart[]> = new Promise(() => []);
	let sliceOptions: Promise<Slice[]> = new Promise(() => []);

	const zenoClient = getContext('zenoClient') as ZenoService;

	$: chartOptions =
		selectedProjects.length > 0
			? zenoClient.getChartsForProjects(selectedProjects)
			: new Promise(() => []);
	$: sliceOptions =
		selectedProjects.length > 0
			? zenoClient.getSlicesForProjects(selectedProjects)
			: new Promise(() => []);

	function deleteElement(elementId: number) {
		if (elementId < 0) return;
		elements = elements.filter((e) => e.id !== elementId);
		zenoClient.deleteReportElement(elementId);
	}

	function addElement(elementIndex: number) {
		zenoClient
			.addReportElement(data.report.id, {
				type: ReportElementType.TEXT,
				data: 'new element',
				position: elementIndex
			})
			.then(
				(res) =>
					(elements = [
						...elements,
						{
							id: res,
							type: ReportElementType.TEXT,
							data: 'new element',
							position: elementIndex
						}
					])
			);
	}

	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	function updateReportName(e: any) {
		zenoClient.updateReport({ ...data.report, name: e.target?.textContent }).then(() => {
			goto('/report/' + data.report.ownerName + '/' + e.target?.textContent);
		});
	}

	function updateReportProjects(e: CustomEvent) {
		const projectUuids = e.detail.map((p: Project) => p.uuid);
		zenoClient.updateReportProjects(data.report.id, projectUuids);
		if (projectUuids.length > 0) {
			chartOptions = zenoClient.getChartsForProjects(projectUuids);
		} else {
			chartOptions = new Promise(() => []);
		}
	}

	function handleDropped(e: CustomEvent) {
		e.detail.items.forEach((item: ReportElement, index: number) => {
			item.position = index;
			zenoClient.updateReportElement(data.report.id, { ...item, position: index });
		});
		elements = e.detail.items;
		dragEnabled = false;
	}

	function handleMoved(e: CustomEvent) {
		elements = e.detail.items;
	}
</script>

<div class="w-full h-full bg-yellowish overflow-scroll">
	<div
		class="flex flex-col max-w-4xl m-auto bg-background px-10 pb-20 md:mt-6 md:mb-6 sm:mt-0 sm:mb-0 rounded shadow"
	>
		<div class="flex items-center mt-12 justify-between">
			<h1
				class="text-5xl mr-6 text-grey-darkest"
				contenteditable={isEdit ? true : false}
				on:blur={(e) => updateReportName(e)}
			>
				{data.report.name}
			</h1>
			{#if data.report.editor}
				<Button variant="raised" on:click={() => (isEdit = !isEdit)}>
					<Label>{isEdit ? 'View' : 'Edit'}</Label>
				</Button>
			{/if}
		</div>
		<h5 class="mt-4 ml-1 text-lg">Author: {data.report.ownerName}</h5>

		{#if isEdit}
			<p class="mt-4 mb-2">Associated Projects</p>
			{#await zenoClient.getProjects() then projects}
				<Svelecte
					bind:value={selectedProjects}
					on:change={updateReportProjects}
					valueField="uuid"
					labelField="name"
					searchable={false}
					multiple={true}
					options={projects}
				/>
			{/await}
		{/if}
		<hr class="mt-6 mb-2 text-grey-light" />
		<div
			class="flex flex-col"
			use:dndzone={{ items: elements, dragDisabled: !dragEnabled }}
			on:consider={handleMoved}
			on:finalize={handleDropped}
		>
			{#each elements as element (element.id)}
				{#if isEdit}
					<ElementEdit
						bind:element
						bind:dragEnabled
						{chartOptions}
						{sliceOptions}
						reportId={data.report.id}
						on:delete={() => deleteElement(element.id ?? -1)}
					/>
				{:else}
					<Element {element} {chartOptions} />
				{/if}
			{/each}
			{#if isEdit}
				<Button variant="raised" on:click={() => addElement(elements.length)}>Add Element</Button>
			{/if}
		</div>
	</div>
</div>
