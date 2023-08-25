<script lang="ts">
	import { ReportElementType, type ReportElement } from '$lib/zenoapi';
	import { mdiCheck, mdiClose, mdiFileEdit, mdiPlus } from '@mdi/js';
	import { Svg } from '@smui/common';
	import IconButton, { Icon } from '@smui/icon-button';
	import { createEventDispatcher } from 'svelte';
	import ChartElement from './ChartElement.svelte';
	import ElementEdit from './ElementEdit.svelte';
	import TextElement from './TextElement.svelte';

	export let element: ReportElement;
	export let isEdit: boolean;

	const dispatch = createEventDispatcher();
	const dispatchUpdate = createEventDispatcher<{
		updateElement: { element: ReportElement };
	}>();

	let elementToEdit = false;
	function deleteElement() {
		dispatch('deleteElement');
	}
	function updateElement() {
		elementToEdit = false;
		dispatchUpdate('updateElement', { element: element });
	}
	function addElement() {
		dispatch('addElement');
	}
</script>

<div class="flex items-center whitespace-nowrap">
	<div class="w-[800px]">
		{#if !elementToEdit}
			{#if element.type === ReportElementType.TEXT}
				<TextElement {element} />
			{:else if element.type === ReportElementType.CHART}
				<ChartElement {element} />
			{/if}
		{:else}
			<ElementEdit bind:element />
		{/if}
	</div>
	{#if isEdit && !elementToEdit}
		<div>
			<IconButton on:click={() => (elementToEdit = true)}>
				<Icon component={Svg} viewBox="0 0 24 24">
					<path fill="black" d={mdiFileEdit} />
				</Icon>
			</IconButton>
			<IconButton on:click={addElement}>
				<Icon component={Svg} viewBox="0 0 24 24">
					<path fill="black" d={mdiPlus} />
				</Icon>
			</IconButton>
			<IconButton on:click={deleteElement}>
				<Icon component={Svg} viewBox="0 0 24 24">
					<path fill="black" d={mdiClose} />
				</Icon>
			</IconButton>
		</div>
	{:else if isEdit && elementToEdit}
		<div>
			<IconButton on:click={updateElement}>
				<Icon component={Svg} viewBox="0 0 24 24">
					<path fill="black" d={mdiCheck} />
				</Icon>
			</IconButton>
		</div>
	{/if}
</div>
