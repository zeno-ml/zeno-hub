<script lang="ts">
	import {
		ReportElementType,
		type Chart,
		type ChartConfig,
		type Report,
		type ReportElement,
		type Slice,
		type Tag
	} from '$lib/zenoapi';
	import {
		mdiCheckBold,
		mdiChevronDown,
		mdiChevronUp,
		mdiPencilOutline,
		mdiTrashCanOutline
	} from '@mdi/js';
	import { Icon } from '@smui/button';
	import AddElementButton from './AddElementButton.svelte';
	import Element from './Element.svelte';
	import ElementEdit from './ElementEdit.svelte';

	export let element: ReportElement;
	export let report: Report;
	export let editId: number;
	export let showConfirmDelete: number;
	export let chartOptions: Chart[] = [];
	export let chartConfigOptions: ChartConfig[] = [];
	export let sliceOptions: Slice[] = [];
	export let tagOptions: Tag[] = [];
	export let addElement: (elementIndex: number) => void;
	export let swapElementPositions: (elementId: number | null | undefined, position: number) => void;
</script>

<div
	class="relative border-2
			{editId === element.id ? 'border-primary-mid' : 'border-white'}
			{report.editor ? 'group/edit rounded p-4 hover:border-primary-mid' : 'py-2'}
			transition"
>
	<button
		class="absolute -top-4 right-14 hidden rounded-md bg-primary-light p-1 transition hover:bg-primary-mid group-hover/edit:block"
		on:click={() => (showConfirmDelete = element.id ?? -1)}
	>
		<Icon style="outline:none; width: 20px; height: 20px" tag="svg" viewBox="0 0 24 24">
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
		<Icon style="outline:none; width: 20px; height: 20px" tag="svg" viewBox="0 0 24 24">
			<path class="fill-primary" d={editId === element.id ? mdiCheckBold : mdiPencilOutline} />
		</Icon>
	</button>
	<button
		class="absolute -left-3 top-1 mr-2 hidden rounded-md bg-primary-light hover:bg-primary-mid group-hover/edit:flex"
		on:click={() => swapElementPositions(element.id, element.position - 1)}
	>
		<Icon style="outline:none; width: 24px; height: 24px" tag="svg" viewBox="0 0 24 24">
			<path class="fill-primary" d={mdiChevronUp} />
		</Icon>
	</button>
	<button
		class="absolute -left-3 top-8 mr-2 hidden rounded-md bg-primary-light hover:bg-primary-mid group-hover/edit:flex"
		on:click={() => swapElementPositions(element.id, element.position + 1)}
	>
		<Icon style="outline:none; width: 24px; height: 24px" tag="svg" viewBox="0 0 24 24">
			<path class="fill-primary" d={mdiChevronDown} />
		</Icon>
	</button>
	{#if editId === element.id}
		<div class={`flex ${element.type === ReportElementType.TEXT ? 'flex-row' : 'flex-col'}`}>
			<div class={element.type === ReportElementType.TEXT ? 'w-1/2' : 'w-full'}>
				<ElementEdit bind:element {chartOptions} {sliceOptions} {tagOptions} reportId={report.id} />
			</div>
			<div class={element.type === ReportElementType.TEXT ? 'w-1/2' : 'w-full'}>
				<Element {element} {chartOptions} {chartConfigOptions} />
			</div>
		</div>
	{:else}
		<Element {element} {chartOptions} {chartConfigOptions} />
	{/if}
</div>
{#if report.editor}
	<AddElementButton position={element.position + 1} {addElement} />
{/if}
