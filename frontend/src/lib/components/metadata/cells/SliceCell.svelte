<script lang="ts">
	import { invalidate } from '$app/navigation';
	import Confirm from '$lib/components/popups/Confirm.svelte';
	import { comparisonModel, model, project, selections, slices } from '$lib/stores';
	import { clickOutside } from '$lib/util/clickOutside';
	import { Join, ZenoService, type Slice } from '$lib/zenoapi';
	import { mdiDotsHorizontal } from '@mdi/js';
	import { Content } from '@smui/dialog';
	import IconButton, { Icon } from '@smui/icon-button';
	import Paper from '@smui/paper';
	import { getContext } from 'svelte';
	import SliceDetails from '../../general/SliceDetails.svelte';
	import SlicePopup from '../../popups/SlicePopup.svelte';
	import SliceCellResult from './SliceCellResult.svelte';

	export let slice: Slice;
	export let compare: boolean;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let showTooltip = false;
	let hovering = false;
	let showOptions = false;
	let editing = false;
	let showConfirmDelete = false;

	$: selected = $selections.slices.includes(slice.id);
	$: transferData =
		$selections.slices.length > 0 && $selections.slices.includes(slice.id)
			? $selections.slices.join(',')
			: [slice.id].join(',');

	function removeSlice() {
		selections.update((m) => {
			for (let key in m.metadata) {
				m.metadata[key] = { predicates: [], join: Join.AND };
			}
			return { slices: [], metadata: { ...m.metadata }, tags: [] };
		});
		zenoClient
			.deleteSlice(slice)
			.then(() => slices.update((s) => s.filter((s) => s.id !== slice.id)));
	}

	function dragStart(e: DragEvent) {
		if (e.dataTransfer !== null) {
			e.dataTransfer.setData('text/plain', transferData);
			e.dataTransfer.dropEffect = 'copy';
		}
	}

	function dragEnd(e: DragEvent) {
		if (e.dataTransfer !== null) {
			// If dragged out of a folder, remove from the folder it was in.
			if (e.dataTransfer.dropEffect === 'none') {
				const data = transferData.split(',');
				data.forEach((element) => {
					const slice = $slices.find((slice) => slice.id === parseInt(element));
					if (slice) {
						zenoClient.updateSlice($project.uuid, { ...slice, folderId: undefined }).then(() =>
							slices.update((s) => {
								invalidate('app:state');
								const index = s.findIndex((s) => s.id === slice.id);
								if (index !== -1) {
									s[index].folderId = undefined;
								}
								return s;
							})
						);
					}
				});
			}
		}
	}

	function selectSliceCell(e: MouseEvent, slice: Slice) {
		if (
			$selections.slices.length === 1 &&
			$selections.slices.some((currentSlice) => currentSlice === slice.id)
		) {
			selections.update((s) => ({
				slices: [],
				metadata: s.metadata,
				tags: s.tags
			}));
			return;
		}
		if (e.shiftKey) {
			if ($selections.slices.some((currentSlice) => currentSlice === slice.id)) {
				selections.update((sel) => {
					sel.slices.splice(
						sel.slices.findIndex((currentSlice) => currentSlice === slice.id),
						1
					);
					return {
						slices: [...sel.slices],
						metadata: sel.metadata,
						tags: sel.tags
					};
				});
			} else {
				selections.update((sel) => ({
					slices: [...sel.slices, slice.id],
					metadata: sel.metadata,
					tags: sel.tags
				}));
			}
		} else {
			selections.update((sel) => ({
				slices: [slice.id],
				metadata: sel.metadata,
				tags: sel.tags
			}));
		}
	}
</script>

{#if editing}
	<SlicePopup on:close={() => (editing = false)} sliceToEdit={slice} />
{/if}
{#if showConfirmDelete}
	<Confirm
		message="Are you sure you want to delete this slice?"
		on:cancel={() => {
			showConfirmDelete = false;
		}}
		on:confirm={() => {
			showConfirmDelete = false;
			removeSlice();
		}}
	/>
{/if}
<button
	class="relative mt-1 flex w-full items-center justify-between overflow-visible rounded border border-grey-lighter px-2.5 text-grey
	{selected ? ' bg-primary-light' : ''} 
	{compare ? ' h-11 py-1' : 'h-9'}"
	on:click={(e) => selectSliceCell(e, slice)}
	on:mouseover={() => (hovering = true)}
	on:focus={() => (hovering = true)}
	on:mouseleave={() => (hovering = false)}
	on:blur={() => (hovering = false)}
	on:dragstart={dragStart}
	on:dragend={dragEnd}
	draggable="true"
>
	{#if showTooltip}
		<div
			class="absolute left-0 top-full z-10 w-fit rounded border border-grey-lighter bg-background p-2 shadow-xl"
		>
			<SliceDetails predicateGroup={slice.filterPredicates} />
		</div>
	{/if}
	<div class="flex w-full items-center justify-between">
		<span
			class="truncate"
			role="tooltip"
			on:mouseover={() => (showTooltip = true)}
			on:mouseout={() => (showTooltip = false)}
			on:focus={() => (showTooltip = true)}
			on:blur={() => (showTooltip = false)}
		>
			{slice.sliceName}
		</span>
		<div
			class="flex items-center"
			use:clickOutside={() => {
				showOptions = false;
			}}
		>
			{#if showOptions}
				<div class="absolute right-0 top-0 z-30 mt-9 hover:bg-grey-lighter">
					<Paper style="padding: 3px 0px;" elevation={7}>
						<Content>
							<button
								class="py flex w-20 items-center px-2 hover:bg-grey-lighter"
								on:click={(e) => {
									e.stopPropagation();
									showOptions = false;
									editing = true;
								}}
							>
								<Icon style="font-size: 18px;" class="material-icons">edit</Icon>&nbsp;
								<span class="text-xs">Edit</span>
							</button>
							<button
								class="py flex w-20 items-center px-2 hover:bg-grey-lighter"
								on:click={(e) => {
									e.stopPropagation();
									showOptions = false;
									showConfirmDelete = true;
								}}
							>
								<Icon style="font-size: 18px;" class="material-icons">delete_outline</Icon>&nbsp;
								<span class="text-xs">Remove</span>
							</button>
						</Content>
					</Paper>
				</div>
			{/if}
			<SliceCellResult {compare} {slice} sliceModel={$model ?? ''} />
			{#if compare}
				<SliceCellResult {compare} {slice} sliceModel={$comparisonModel ?? ''} />
			{/if}
			{#if $project.editor}
				<div
					class="min-w-[36px]"
					use:clickOutside={() => {
						hovering = false;
					}}
				>
					{#if hovering}
						<IconButton
							class="p-0"
							size="button"
							on:click={(e) => {
								e.stopPropagation();
								showOptions = !showOptions;
							}}
						>
							<Icon tag="svg" viewBox="0 0 24 24">
								<path fill="black" d={mdiDotsHorizontal} />
							</Icon>
						</IconButton>
					{/if}
				</div>
			{/if}
		</div>
	</div>
</button>
