<script lang="ts">
	import {
		ReportElementType,
		ZenoService,
		type Chart,
		type Report,
		type ReportElement,
		type Slice
	} from '$lib/zenoapi';
	import { mdiCheckBold, mdiDrag, mdiPencilOutline, mdiTrashCanOutline } from '@mdi/js';
	import { Icon } from '@smui/button';
	import { getContext } from 'svelte';
	import AddElementButton from './AddElementButton.svelte';
	import Element from './Element.svelte';
	import ElementEdit from './ElementEdit.svelte';

	export let element: ReportElement;
	export let report: Report;
	export let selectedProjects: string[];
	export let editId: number;
	export let showConfirmDelete: number;
	export let dragEnabled: boolean;
	export let addElement: (elementIndex: number) => void;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let chartOptions: Chart[] = [];
	let sliceOptions: Slice[] = [];

	$: if (selectedProjects.length > 0) {
		zenoClient.getChartsForProjects(selectedProjects).then((r) => (chartOptions = r));
	}
	$: if (selectedProjects.length > 0) {
		zenoClient.getSlicesForProjects(selectedProjects).then((r) => (sliceOptions = r));
	}
</script>

<div>
	<div
		class="relative border-2
			{editId === element.id ? 'border-primary-mid' : 'border-white'}
			{report.editor ? 'group/edit rounded p-4 hover:border-primary-mid' : 'py-2'}
			{dragEnabled ? 'border-2 border-primary-mid' : ''} transition"
	>
		<button
			class="absolute -top-4 right-14 hidden rounded-md bg-primary-light p-1 transition hover:bg-primary-mid group-hover/edit:block"
			on:click={() => (showConfirmDelete = element.id ?? -1)}
		>
			<Icon
				style="outline:none; width: 20px; height: 20px"
				tag="svg"
				viewBox="0 0 24 24"
				on:mousedown={() => (dragEnabled = true)}
			>
				<path class="fill-primary" d={mdiTrashCanOutline} />
			</Icon>
		</button>
		<button
			class="absolute -top-4 right-4 hidden rounded-md bg-primary-light p-1 transition hover:bg-primary-mid group-hover/edit:block"
			on:click={() =>
				editId === element.id || element.id === null || element.id === undefined
					? (editId = -1)
					: (editId = element.id)}
		>
			<Icon
				style="outline:none; width: 20px; height: 20px"
				tag="svg"
				viewBox="0 0 24 24"
				on:mousedown={() => (dragEnabled = true)}
			>
				<path class="fill-primary" d={editId === element.id ? mdiCheckBold : mdiPencilOutline} />
			</Icon>
		</button>
		<div
			class="absolute -left-3 top-1 mr-2 hidden cursor-move rounded-md bg-primary-light hover:bg-primary-mid group-hover/edit:flex"
		>
			<Icon
				style="outline:none; width: 24px; height: 24px"
				tag="svg"
				viewBox="0 0 24 24"
				on:mousedown={() => (dragEnabled = true)}
			>
				<path class="fill-primary" d={mdiDrag} />
			</Icon>
		</div>
		{#if editId === element.id}
			<div class={`flex ${element.type === ReportElementType.TEXT ? 'flex-row' : 'flex-col'}`}>
				<div class={element.type === ReportElementType.TEXT ? 'w-1/2' : 'w-full'}>
					{#await sliceOptions then sliceOptions}
						<ElementEdit bind:element {chartOptions} {sliceOptions} reportId={report.id} />
					{/await}
				</div>
				<div class={element.type === ReportElementType.TEXT ? 'w-1/2' : 'w-full'}>
					<Element {element} {chartOptions} />
				</div>
			</div>
		{:else}
			<Element {element} {chartOptions} />
		{/if}
	</div>
	{#if report.editor}
		<AddElementButton position={element.position + 1} {addElement} />
	{/if}
</div>
