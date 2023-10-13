<script lang="ts">
	import type { Chart, Report, ReportElement, Slice } from '$lib/zenoapi';
	import { mdiDrag } from '@mdi/js';
	import { Icon } from '@smui/button';
	import AddElementButton from './AddElementButton.svelte';
	import Element from './Element.svelte';
	import ElementEdit from './ElementEdit.svelte';

	export let element: ReportElement;
	export let report: Report;
	export let chartOptions: Promise<Chart[]>;
	export let sliceOptions: Promise<Slice[]>;
	export let editId: number;
	export let showConfirmDelete: number;
	export let dragEnabled: boolean;
	export let addElement: (elementIndex: number) => void;
</script>

<div>
	<div
		class="border-2 relative
			{editId === element.id ? 'border-primary-mid' : 'border-white'}
			{report.editor ? 'group/edit hover:border-primary-mid rounded p-4' : 'py-2'}
			{dragEnabled ? 'border-primary-mid border-2' : ''} transition"
	>
		<button
			class="group-hover/edit:block hidden px-4 py-1 border-primary-mid border-2 absolute bg-white -top-4 rounded-md hover:bg-primary-light transition"
			on:click={() =>
				editId === element.id || element.id === null || element.id === undefined
					? (editId = -1)
					: (editId = element.id)}
		>
			{editId === element.id ? 'done' : 'edit'}
		</button>
		<button
			class="group-hover/edit:block hidden px-4 py-1 border-primary-mid border-2 absolute bg-white -top-4 right-4 rounded-md hover:bg-primary-light transition"
			on:click={() => (showConfirmDelete = element.id ?? -1)}
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
			<ElementEdit bind:element {chartOptions} {sliceOptions} reportId={report.id} />
		{:else}
			<Element {element} {chartOptions} />
		{/if}
	</div>
	{#if report.editor}
		<AddElementButton position={element.position + 1} {addElement} />
	{/if}
</div>