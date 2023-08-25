<script lang="ts">
	import Element from '$lib/components/report/Element.svelte';
	import { report } from '$lib/stores';
	import { ZenoService, type ReportElement } from '$lib/zenoapi';
	import Button, { Label } from '@smui/button';
	import CircularProgress from '@smui/circular-progress/src/CircularProgress.svelte';

	$: elementRequest = $report ? ZenoService.getReportElements($report.id) : undefined;

	let isEdit = false;

	function deleteElement(elementIndex: number) {
		ZenoService.deleteReportElement(elementIndex).then(() => {
			if ($report) {
				elementRequest = ZenoService.getReportElements($report.id);
			}
		});
	}

	function addElement(elementIndex: number) {
		elements = [
			...report.elements.slice(0, elementIndex + 1),
			{
				type: ReportTextElementType.TEXT,
				text: 'new element'
			},
			...report.elements.slice(elementIndex + 1)
		];
	}

	function updateElement(event: CustomEvent<{ element: ReportElement }>) {
		ZenoService.updateReportElement(event.element).then(() => {
			if ($report) elementRequest = ZenoService.getReportElements($report.id);
		});
	}
</script>

{#if $report}
	<div class="flex flex-col ml-12 h-full">
		{#if $report.editor}
			<Button
				style="width: 24px; height: 24px;background-color:var(--G5);position:absolute;right:50px;top:10px"
				on:mouseleave={blur}
				on:focusout={blur}
				on:click={() => (isEdit = !isEdit)}
			>
				<Label>{isEdit ? 'View' : 'Edit'}</Label>
			</Button>
		{/if}
		<h1>{$report?.name}</h1>
		<div class="flex flex-col overflow-y-auto py-5">
			{#await elementRequest}
				<CircularProgress style="height: 32px; width: 32px; margin-right:20px" indeterminate />
			{:then elements}
				{#if elements}
					{#each elements as element}
						<Element
							{element}
							{isEdit}
							on:addElement={() => addElement(element.id)}
							on:deleteElement={() => deleteElement(element.id)}
							on:updateElement={updateElement}
						/>
					{/each}
				{/if}
			{/await}
		</div>
	</div>
{/if}
