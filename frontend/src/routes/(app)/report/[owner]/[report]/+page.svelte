<script lang="ts">
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
	import { mdiDrag } from '@mdi/js';
	import Button, { Icon } from '@smui/button';
	import Svelecte from 'svelecte';
	import { getContext } from 'svelte';
	import { dndzone } from 'svelte-dnd-action';

	export let data;

	let elements = data.reportElements.sort((a, b) => a.position - b.position);
	let selectedProjects = data.report.linkedProjects ?? [];
	let editId = -1;
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
			<h1 class="text-5xl mr-6 text-grey-darkest">
				{data.report.name}
			</h1>
		</div>
		<h5 class="mt-4 ml-1 text-lg">Author: {data.report.ownerName}</h5>

		{#if data.report.editor}
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
		<div
			class="flex flex-col hover:border-primary-mid"
			use:dndzone={{ items: elements, dragDisabled: !dragEnabled }}
			on:consider={handleMoved}
			on:finalize={handleDropped}
		>
			{#each elements as element (element.id)}
				<div
					class="border-2 hover:border-primary-mid rounded p-4 relative {editId === element.id
						? 'border-primary-mid'
						: 'border-white'}
					{data.report.editor ? 'group/edit' : ''}"
				>
					<button
						class="group-hover/edit:block hidden px-4 py-1 border-primary-mid border-2 absolute bg-white -top-4 rounded-md"
						on:click={() =>
							editId === element.id || element.id === null || element.id === undefined
								? (editId = -1)
								: (editId = element.id)}
					>
						{editId === element.id ? 'done' : 'edit'}
					</button>
					<button
						class="group-hover/edit:block hidden px-4 py-1 border-primary-mid border-2 absolute bg-white -top-4 right-4 rounded-md"
						on:click={() => deleteElement(element.id ?? -1)}
					>
						{'delete'}
					</button>
					<div
						class="group-hover/edit:flex hidden mr-2 cursor-move absolute -left-3 bg-white border-primary-mid border-2 rounded-md"
					>
						<Icon
							style="outline:none; width: 24px; height: 24px"
							tag="svg"
							viewBox="0 0 24 24"
							on:mousedown={() => (dragEnabled = true)}
						>
							<path fill="black" d={mdiDrag} />
						</Icon>
					</div>
					{#if editId === element.id}
						<ElementEdit bind:element {chartOptions} {sliceOptions} reportId={data.report.id} />
					{:else}
						<Element {element} {chartOptions} />
					{/if}
				</div>
			{/each}
			<br />
			{#if data.report.editor}
				<Button variant="raised" on:click={() => addElement(elements.length)}>Add Element</Button>
			{/if}
		</div>
	</div>
</div>
