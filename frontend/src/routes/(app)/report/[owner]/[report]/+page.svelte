<script lang="ts">
	import { goto, invalidate } from '$app/navigation';
	import Element from '$lib/components/report/Element.svelte';
	import { ReportElementType, ZenoService, type Chart, type ReportElement } from '$lib/zenoapi';
	import Button, { Label } from '@smui/button';
	import Svelecte from 'svelecte';

	export let data;

	let selectedProjects = data.report.linkedProjects ?? [];
	let chartOptions: Promise<Chart[]> =
		selectedProjects.length > 0
			? ZenoService.getChartsForProjects(selectedProjects)
			: new Promise(() => []);
	let isEdit = false;

	$: report = data.report;
	$: elements = data.reportElements;
	$: updateReportProjects(selectedProjects);

	function deleteElement(elementIndex: number) {
		if (elementIndex < 0) return;
		ZenoService.deleteReportElement(elementIndex).then(() => invalidate('app:report'));
	}

	function addElement(elementIndex: number) {
		ZenoService.addReportElement(report.id, {
			type: ReportElementType.TEXT,
			data: 'new element',
			position: elementIndex
		}).then(() => invalidate('app:report'));
	}

	function updateElement(event: CustomEvent<{ element: ReportElement }>) {
		ZenoService.updateReportElement(report.id, event.detail.element as ReportElement).then(() =>
			invalidate('app:report')
		);
	}

	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	function updateReportName(e: any) {
		ZenoService.updateReport({ ...report, name: e.target?.textContent }).then(() => {
			goto('/report/' + report.ownerName + '/' + e.target?.textContent);
		});
	}

	function updateReportProjects(project_uuids: string[]) {
		ZenoService.updateReportProjects(report.id, project_uuids);
		if (project_uuids.length > 0) chartOptions = ZenoService.getChartsForProjects(project_uuids);
	}
</script>

<div class="w-full bg-yellowish overflow-scroll">
	<div class="flex flex-col max-w-4xl m-auto bg-background px-10 pb-20 mt-10 rounded shadow">
		<div class="flex items-center mt-12 justify-between">
			<h1
				class="text-4xl mr-6"
				contenteditable={isEdit ? true : false}
				on:blur={(e) => updateReportName(e)}
			>
				{report.name}
			</h1>
			{#if report.editor}
				<Button
					variant="raised"
					on:mouseleave={blur}
					on:focusout={blur}
					on:click={() => (isEdit = !isEdit)}
				>
					<Label>{isEdit ? 'View' : 'Edit'}</Label>
				</Button>
			{/if}
		</div>

		{#if isEdit}
			<div>
				<p class="mt-4 mb-2">Associated Projects</p>
				{#await ZenoService.getProjects() then projects}
					<Svelecte
						bind:value={selectedProjects}
						searchable={false}
						multiple={true}
						options={projects}
					/>
				{/await}
			</div>
		{/if}
		<hr class="mt-6 mb-2 text-grey-light" />
		<div class="flex flex-col overflow-y-auto">
			{#each elements.sort((a, b) => a.position - b.position) as element (element.id)}
				<Element
					{element}
					{isEdit}
					{chartOptions}
					on:update={updateElement}
					on:delete={() => deleteElement(element.id ?? -1)}
				/>
			{/each}
			{#if isEdit}
				<Button variant="raised" on:click={() => addElement(elements.length)}>Add Element</Button>
			{/if}
		</div>
	</div>
</div>
