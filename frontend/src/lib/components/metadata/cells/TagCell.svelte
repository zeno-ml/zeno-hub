<script lang="ts">
	import Confirm from '$lib/components/popups/Confirm.svelte';
	import {
		editTag,
		metric,
		model,
		project,
		selectionIds,
		selections,
		tagIds,
		tags
	} from '$lib/stores';
	import { clickOutside } from '$lib/util/clickOutside';
	import { Join, ZenoService, type Tag, type TagMetricKey } from '$lib/zenoapi';
	import { mdiDotsHorizontal } from '@mdi/js';
	import IconButton, { Icon } from '@smui/icon-button';
	import Paper, { Content } from '@smui/paper';
	import { getContext } from 'svelte';

	export let tag: Tag;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let hovering = false;
	let showOptions = false;
	let showConfirmDelete = false;

	$: result = zenoClient.getMetricForTag($project.uuid, <TagMetricKey>{
		tag: tag,
		model: $model,
		metric: $metric?.id || -1
	});
	$: selected = $selections.tags.includes(tag.id);

	function removeTag() {
		selections.update((m) => {
			for (let key in m.metadata) {
				m.metadata[key] = { predicates: [], join: Join.AND };
			}
			return { slices: [], metadata: { ...m.metadata }, tags: [] };
		});
		zenoClient.deleteTag($project.uuid, tag.id).then(() => {
			tags.update((t) => t.filter((t) => t.id !== tag.id));
		});
		tagIds.set([]);
	}

	function updateTagIdsAfterRemove(selectionTags: number[]) {
		let s = new Set<string>();
		//loop through all selectedTags and re-add their IDs (assumes that the selections.tags will already be updated)
		//this is to catch for the case when you have intersections between tags
		selectionTags.forEach((tagId) => {
			const currentTag = $tags.find((tag) => tag.id === tagId);
			if (currentTag !== undefined) currentTag.dataIds.forEach((id) => s.add(id));
		});
		tagIds.set([...s]);
	}

	function addTagIdsToTagIds(tag: Tag) {
		let s = new Set<string>();
		if ($tagIds !== undefined) $tagIds.forEach((id) => s.add(id));
		tag.dataIds.forEach((id) => s.add(id));
		tagIds.set([...s]);
	}

	function setSelected(e: MouseEvent) {
		// Imitate selections in Vega bar charts.
		if ($selections.tags.length === 1 && $selections.tags.includes(tag.id)) {
			// deselect single tag cell
			selections.update((s) => {
				tagIds.set([]);
				return {
					slices: s.slices,
					metadata: s.metadata,
					tags: []
				};
			});
			return;
		}
		if (e.shiftKey) {
			// remove selection in multi-select mode
			if ($selections.tags.includes(tag.id)) {
				selections.update((sel) => {
					sel.tags.splice(sel.tags.indexOf(tag.id), 1);
					updateTagIdsAfterRemove(sel.tags);
					return {
						slices: sel.slices,
						metadata: sel.metadata,
						tags: [...sel.tags]
					};
				});
			}
			// add selection in multi-select mode
			else {
				selections.update((sel) => {
					addTagIdsToTagIds(tag);
					return {
						slices: sel.slices,
						metadata: sel.metadata,
						tags: [...sel.tags, tag.id]
					};
				});
			}
		} else {
			// single select mode
			if ($selections.tags.includes(tag.id)) {
				if ($selections.tags.length > 0) {
					selections.update((sel) => {
						tagIds.set([]);
						addTagIdsToTagIds(tag);
						return {
							slices: sel.slices,
							metadata: sel.metadata,
							tags: [tag.id]
						};
					});
				} else {
					selections.update((sel) => {
						sel.tags.splice(sel.tags.indexOf(tag.id), 1);
						updateTagIdsAfterRemove(sel.tags);
						return {
							slices: sel.slices,
							metadata: sel.metadata,
							tags: [...sel.tags]
						};
					});
				}
			} else {
				selections.update((sel) => {
					tagIds.set([]);
					addTagIdsToTagIds(tag);
					return {
						slices: sel.slices,
						metadata: sel.metadata,
						tags: [tag.id]
					};
				});
			}
		}
	}

	function dragStart(event: DragEvent) {
		if (event.dataTransfer !== null) {
			event.dataTransfer.setData('text/plain', tag.tagName);
			event.dataTransfer.dropEffect = 'copy';
		}
	}
</script>

{#if showConfirmDelete}
	<Confirm
		message="Are you sure you want to delete this tag?"
		on:cancel={() => {
			showConfirmDelete = false;
		}}
		on:confirm={() => {
			removeTag();
			showConfirmDelete = false;
		}}
	/>
{/if}
<button
	class="relative mt-1 flex h-9 w-full items-center justify-between overflow-visible rounded border border-grey-lighter px-2.5 {selected
		? 'bg-greenish-light'
		: ''}"
	on:click={setSelected}
	draggable="true"
	on:mouseover={() => (hovering = true)}
	on:focus={() => (hovering = true)}
	on:mouseleave={() => (hovering = false)}
	on:blur={() => (hovering = false)}
	on:dragstart={dragStart}
>
	<div class="flex w-full items-center justify-between">
		<span>
			{tag.tagName}
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
							{#if $editTag === undefined}
								<button
									class="py flex w-24 items-center px-2 hover:bg-grey-lighter"
									on:keydown={() => ({})}
									on:click={(e) => {
										e.stopPropagation();
										showOptions = false;
										editTag.set(tag);
										selectionIds.set(tag.dataIds);
									}}
								>
									<Icon style="font-size: 18px;" class="material-icons">edit</Icon>&nbsp;
									<span class="text-xs">Edit</span>
								</button>
							{/if}
							<button
								class="py flex w-24 items-center px-2 hover:bg-grey-lighter"
								on:click={(e) => {
									e.stopPropagation();
									showOptions = false;
									navigator.clipboard.writeText(`[${tag.dataIds.toString()}]`);
								}}
							>
								<Icon style="font-size: 18px;" class="material-icons">content_copy</Icon>&nbsp;
								<span class="text-xs">Copy Ids</span>
							</button>
							<button
								class="py flex w-24 items-center px-2 hover:bg-grey-lighter"
								on:keydown={() => ({})}
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
			{#await result then res}
				{#if res !== null && tag.dataIds.length > 0}
					<span class="mr-2 w-full">
						{res.metric !== undefined && res.metric !== null ? res.metric.toFixed(2) : ''}
					</span>
					<span class="mr-1 italic text-grey-darker">
						({res.size.toLocaleString()})
					</span>
				{:else}
					<span class="mr-1 italic text-grey-darker"> (0) </span>
				{/if}
			{/await}
			{#if $project.editor}
				<div
					class="w-[36px] min-w-[36px]"
					use:clickOutside={() => {
						hovering = false;
					}}
				>
					{#if hovering && ($editTag === undefined || $editTag.id !== tag.id)}
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
