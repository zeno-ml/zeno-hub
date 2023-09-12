<script lang="ts">
	import { invalidate } from '$app/navigation';
	import Element from '$lib/components/report/Element.svelte';
	import { ReportElementType, ZenoService } from '$lib/zenoapi';
	import Button, { Label } from '@smui/button';

	export let data;

	let isEdit = false;

	$: report = data.report;
	$: elements = data.reportElements;

	function deleteElement(elementIndex: number) {
		ZenoService.deleteReportElement(elementIndex).then(() => invalidate('app:report'));
	}

	function addElement(elementIndex: number) {
		ZenoService.addReportElement(report.id, {
			type: ReportElementType.TEXT,
			data: 'new element',
			position: elementIndex
		}).then(() => invalidate('app:report'));
	}

	// function updateElement(event: CustomEvent<{ element: ReportElement }>) {
	// 	ZenoService.updateReportElement(event.element).then(() => {
	// 		if ($report) elementRequest = ZenoService.getReportElements($report.id);
	// 	});
	// }
</script>

<div class="flex flex-col ml-12 h-full">
	{#if report.editor}
		<Button
			style="width: 24px; height: 24px;background-color:var(--G5);position:absolute;right:50px;top:10px"
			on:mouseleave={blur}
			on:focusout={blur}
			on:click={() => (isEdit = !isEdit)}
		>
			<Label>{isEdit ? 'View' : 'Edit'}</Label>
		</Button>
	{/if}
	<h1>{report.name}</h1>
	<div class="flex flex-col overflow-y-auto py-5">
		{#each elements as element}
			<Element {element} {isEdit} />
		{/each}
		{#if isEdit}
			<button on:click={() => addElement(0)}>Add Element</button>
		{/if}
	</div>
</div>
