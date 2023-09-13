<script lang="ts">
	import { invalidate } from '$app/navigation';
	import Element from '$lib/components/report/Element.svelte';
	import { ReportElementType, ZenoService, type ReportElement } from '$lib/zenoapi';
	import Button, { Label } from '@smui/button';

	export let data;

	let isEdit = false;

	$: report = data.report;
	$: elements = data.reportElements;

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
</script>

<div class="w-full bg-primary-light">
	<div class="flex flex-col h-full max-w-4xl m-auto bg-background px-10">
		<div class="flex items-center mt-12">
			<h1 class="text-4xl mr-6" contenteditable={isEdit ? true : false}>
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
		<div class="flex flex-col overflow-y-auto py-5">
			{#each elements as element}
				<Element
					{element}
					{isEdit}
					on:update={updateElement}
					on:delete={() => deleteElement(element.id ?? -1)}
				/>
			{/each}
			{#if isEdit}
				<Button style="background-color:var(--G5);" on:click={() => addElement(0)}
					>Add Element</Button
				>
			{/if}
		</div>
	</div>
</div>
