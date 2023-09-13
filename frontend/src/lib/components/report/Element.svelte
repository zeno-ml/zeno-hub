<script lang="ts">
	import { ReportElementType, type ReportElement } from '$lib/zenoapi';
	import { mdiCheck, mdiClose, mdiFileEdit } from '@mdi/js';
	import { Svg } from '@smui/common';
	import IconButton, { Icon } from '@smui/icon-button';
	import { createEventDispatcher } from 'svelte';
	import ChartElement from './ChartElement.svelte';
	import ElementEdit from './ElementEdit.svelte';
	import TextElement from './TextElement.svelte';

	export let element: ReportElement;
	export let isEdit: boolean;

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

<div class="flex items-center whitespace-nowrap my-5">
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
			<IconButton on:click={() => dispatch('delete')}>
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
