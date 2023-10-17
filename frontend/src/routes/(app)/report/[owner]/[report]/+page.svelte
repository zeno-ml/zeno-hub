<script lang="ts">
	import Confirm from '$lib/components/popups/Confirm.svelte';
	import AddElementButton from '$lib/components/report/AddElementButton.svelte';
	import ElementContainer from '$lib/components/report/ElementContainer.svelte';
	import {
		ReportElementType,
		ZenoService,
		type Chart,
		type Project,
		type ReportElement,
		type Slice
	} from '$lib/zenoapi';
	import Svelecte from 'svelecte';
	import { getContext } from 'svelte';
	import { dndzone } from 'svelte-dnd-action';

	export let data;

	let elements = data.reportElements.sort((a, b) => a.position - b.position);
	let selectedProjects = data.report.linkedProjects ?? [];
	let editId = -1;
	let showConfirmDelete = -1;
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
			.then((res) => {
				elements.filter((d) => d.position >= elementIndex).forEach((d) => d.position++);
				elements.push({
					id: res,
					type: ReportElementType.TEXT,
					data: 'new element',
					position: elementIndex
				});
				elements = elements.sort((a, b) => a.position - b.position);
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

{#if showConfirmDelete !== -1}
	<Confirm
		message="Are you sure you want to delete this element?"
		on:cancel={() => {
			showConfirmDelete = -1;
		}}
		on:confirm={() => {
			deleteElement(showConfirmDelete);
			showConfirmDelete = -1;
		}}
	/>
{/if}
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
		<hr class="mt-4 bg-grey-dark" />

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
			<hr class="mt-4 mb-4 bg-grey-dark" />
			<AddElementButton
				position={0}
				{addElement}
				alwaysShow={elements.length === 0 ? true : false}
			/>
		{/if}
		<div
			class="flex flex-col mt-2"
			use:dndzone={{
				items: elements,
				dragDisabled: !dragEnabled,
				dropTargetStyle: {},
				flipDurationMs: 100
			}}
			on:consider={handleMoved}
			on:finalize={handleDropped}
		>
			{#await chartOptions then chartOptions}
				{#await sliceOptions then sliceOptions}
					{#each elements as element (element.id)}
						<ElementContainer
							bind:element
							bind:editId
							bind:dragEnabled
							bind:showConfirmDelete
							{addElement}
							{chartOptions}
							{sliceOptions}
							report={data.report}
						/>
					{/each}
				{/await}
			{/await}
		</div>
	</div>
</div>
