<script lang="ts">
	import { goto } from '$app/navigation';
	import Element from '$lib/components/report/Element.svelte';
	import ElementEdit from '$lib/components/report/ElementEdit.svelte';
	import { report } from '$lib/stores.js';
	import {
		ReportElementType,
		ZenoService,
		type Chart,
		type Project,
		type ReportElement
	} from '$lib/zenoapi';
	import Button, { Label } from '@smui/button';
	import Svelecte from 'svelecte';
	import { dndzone } from 'svelte-dnd-action';

	export let data;

	// Only set stores the report has changed.
	if ($report === undefined || $report.id !== data.report.id) {
		report.set(data.report);
	}

	let elements = data.reportElements.sort((a, b) => a.position - b.position);
	let selectedProjects = data.report.linkedProjects ?? [];
	let chartOptions: Promise<Chart[]> =
		selectedProjects.length > 0
			? ZenoService.getChartsForProjects(selectedProjects)
			: new Promise(() => []);
	let isEdit = false;
	let dragEnabled = false;

	function deleteElement(elementId: number) {
		if (elementId < 0) return;
		elements = elements.filter((e) => e.id !== elementId);
		ZenoService.deleteReportElement(elementId);
	}

	function addElement(elementIndex: number) {
		ZenoService.addReportElement($report.id, {
			type: ReportElementType.TEXT,
			data: 'new element',
			position: elementIndex
		}).then(
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
		ZenoService.updateReport({ ...$report, name: e.target?.textContent }).then(() => {
			goto('/report/' + $report.ownerName + '/' + e.target?.textContent);
		});
	}

	function updateReportProjects(e: CustomEvent) {
		const projectUuids = e.detail.map((p: Project) => p.uuid);
		ZenoService.updateReportProjects($report.id, projectUuids);
		if (projectUuids.length > 0) {
			chartOptions = ZenoService.getChartsForProjects(projectUuids);
		} else {
			chartOptions = new Promise(() => []);
		}
	}

	function handleDropped(e: CustomEvent) {
		e.detail.items.forEach((item: ReportElement, index: number) => {
			item.position = index;
			ZenoService.updateReportElement($report.id, { ...item, position: index });
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
				{$report.name}
			</h1>
			{#if $report.editor}
				<Button variant="raised" on:click={() => (isEdit = !isEdit)}>
					<Label>{isEdit ? 'View' : 'Edit'}</Label>
				</Button>
			{/if}
		</div>
		<h5 class="mt-4 ml-1 text-lg">Author: {$report.ownerName}</h5>

		{#if isEdit}
			<p class="mt-4 mb-2">Associated Projects</p>
			{#await ZenoService.getProjects() then projects}
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
						{element}
						bind:dragEnabled
						reportId={$report.id}
						{chartOptions}
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
