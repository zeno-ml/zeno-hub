<script lang="ts">
	import {
		ReportElementType,
		ZenoService,
		type Chart,
		type Project,
		type Report,
		type ReportElement,
		type Slice
	} from '$lib/zenoapi';
	import { mdiDrag } from '@mdi/js';
	import { Icon } from '@smui/button';
	import { getContext } from 'svelte';
	import AddElementButton from './AddElementButton.svelte';
	import Element from './Element.svelte';
	import ElementEdit from './ElementEdit.svelte';

	export let element: ReportElement;
	export let report: Report;
	export let reportProjects: Project[];
	export let editId: number;
	export let showConfirmDelete: number;
	export let dragEnabled: boolean;
	export let addElement: (elementIndex: number) => void;

	const zenoClient = getContext('zenoClient') as ZenoService;

	$: chartOptions = (
		reportProjects.length > 0
			? zenoClient.getChartsForProjects(reportProjects.map((p) => p.uuid))
			: new Promise(() => [] as Chart[])
	) as Promise<Chart[]>;
	$: sliceOptions = (
		reportProjects.length > 0
			? zenoClient.getSlicesForProjects(reportProjects.map((p) => p.uuid))
			: new Promise(() => [] as Slice[])
	) as Promise<Slice[]>;
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
		{#await chartOptions then chartOptions}
			{#if editId === element.id}
				<div class={`flex ${element.type === ReportElementType.TEXT ? 'flex-row' : 'flex-col'}`}>
					<div class={element.type === ReportElementType.TEXT ? 'w-1/2' : 'w-full'}>
						{#await sliceOptions then sliceOptions}
							<ElementEdit
								bind:element
								{chartOptions}
								{sliceOptions}
								{reportProjects}
								reportId={report.id}
							/>
						{/await}
					</div>
					<div class={element.type === ReportElementType.TEXT ? 'w-1/2' : 'w-full'}>
						<Element {element} {chartOptions} />
					</div>
				</div>
			{:else}
				<Element {element} {chartOptions} />
			{/if}
		{/await}
	</div>
	{#if report.editor}
		<AddElementButton position={element.position + 1} {addElement} />
	{/if}
</div>
