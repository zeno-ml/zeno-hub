<script lang="ts">
	import { ReportElementType, type Chart, type ReportElement } from '$lib/zenoapi';
	import { mdiCheck, mdiClose, mdiFileEdit } from '@mdi/js';
	import { SmuiElement } from '@smui/common';
	import IconButton from '@smui/icon-button';
	import { createEventDispatcher } from 'svelte';
	import ChartElement from './ChartElement.svelte';
	import ElementEdit from './ElementEdit.svelte';
	import TextElement from './TextElement.svelte';

	export let element: ReportElement;
	export let isEdit: boolean;
	export let chartOptions: Promise<Chart[]>;

	let elementToEdit = false;

	const dispatch = createEventDispatcher();
	const dispatchUpdate = createEventDispatcher<{
		update: { element: ReportElement };
	}>();

	function updateElement() {
		elementToEdit = false;
		dispatchUpdate('update', { element: element });
	}
</script>

<div class="flex items-center my-5">
	<div class="w-[800px]">
		{#if !elementToEdit}
			{#if element.type === ReportElementType.TEXT}
				<TextElement {element} />
			{:else if element.type === ReportElementType.CHART}
				{#await chartOptions then options}
					<ChartElement chart={options.filter((c) => c.id === element.chartId)[0]} />
				{/await}
			{/if}
		{:else}
			<ElementEdit bind:element {chartOptions} />
		{/if}
	</div>
	{#if isEdit && !elementToEdit}
		<div>
			<IconButton on:click={() => (elementToEdit = true)}>
				<SmuiElement tag="svg" viewBox="0 0 24 24">
					<path fill="black" d={mdiFileEdit} />
				</SmuiElement>
			</IconButton>
			<IconButton on:click={() => dispatch('delete')}>
				<SmuiElement tag="svg" viewBox="0 0 24 24">
					<path fill="black" d={mdiClose} />
				</SmuiElement>
			</IconButton>
		</div>
	{:else if isEdit && elementToEdit}
		<div>
			<IconButton on:click={updateElement}>
				<SmuiElement tag="svg" viewBox="0 0 24 24">
					<path fill="black" d={mdiCheck} />
				</SmuiElement>
			</IconButton>
		</div>
	{/if}
</div>
