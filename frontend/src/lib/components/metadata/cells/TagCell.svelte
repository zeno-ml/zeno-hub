<script lang="ts">
	import { getMetricsForTags } from '$lib/api/tag';
	import { editTag, metric, model, projectConfig, selections, tagIds, tags } from '$lib/stores';
	import { clickOutside } from '$lib/util/clickOutside';
	import { Join, ZenoService, type Tag, type TagMetricKey } from '$lib/zenoapi';
	import { mdiDotsHorizontal } from '@mdi/js';
	import IconButton, { Icon } from '@smui/icon-button';
	import Paper, { Content } from '@smui/paper';

	export let tag: Tag;
	export let inFolder = false;

	let hovering = false;
	let showOptions = false;

	$: result = getMetricsForTags(<TagMetricKey>{
		tag: tag,
		model: $model,
		metric: $metric
	});
	$: selected = $selections.tags.includes(tag.id);

	function removeTag() {
		selections.update((m) => {
			for (let key in m.metadata) {
				m.metadata[key] = { predicates: [], join: Join.AND };
			}
			return { slices: [], metadata: { ...m.metadata }, tags: [] };
		});
		ZenoService.deleteTag(tag).then(() => {
			if ($projectConfig !== undefined) {
				ZenoService.getTags($projectConfig.uuid).then((fetchedTags) => tags.set(fetchedTags));
			}
		});
		tagIds.set([]);
	}

	function updateTagIdsAfterRemove(selectionTags: number[]) {
		let s = new Set<string>();
		//loop through all selectedTags and re-add their IDs (assumes that the selections.tags will already be updated)
		//this is to catch for the case when you have intersections between tags
		selectionTags.forEach((tagId) => {
			const currentTag = $tags.find((tag) => tag.id === tagId);
			if (currentTag !== undefined) currentTag.items.forEach((id) => s.add(id));
		});
		tagIds.set([...s]);
	}

	function addTagIdsToTagIds(tag: Tag) {
		let s = new Set<string>();
		if ($tagIds !== undefined) $tagIds.forEach((id) => s.add(id));
		tag.items.forEach((id) => s.add(id));
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

<button
	class="relative border border-grey-lighter rounded-2xl mt-1 flex items-center justify-between px-2.5 parent h-9 overflow-visible w-full {selected
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
	<div class="flex justify-between items-center w-full">
		<span>
			{tag.tagName}
		</span>
		<div
			class="flex justify-between items-center"
			use:clickOutside={() => {
				showOptions = false;
			}}
		>
			{#if showOptions}
				<div class="top-0 right-0 absolute mt-9 hover:bg-grey-lighter z-30">
					<Paper style="padding: 3px 0px;" elevation={7}>
						<Content>
							{#if $editTag === undefined}
								<div
									class="flex items-center w-20 py px-2 hover:bg-grey-lighter"
									on:keydown={() => ({})}
									on:click={(e) => {
										e.stopPropagation();
										showOptions = false;
										editTag.set(tag);
									}}
								>
									<Icon style="font-size: 18px;" class="material-icons">edit</Icon>&nbsp;
									<span class="text-xs">Edit</span>
								</div>
							{/if}
							<div
								class="flex items-center w-20 py px-2 hover:bg-grey-lighter"
								on:keydown={() => ({})}
								on:click={(e) => {
									e.stopPropagation();
									showOptions = false;
									removeTag();
								}}
							>
								<Icon style="font-size: 18px;" class="material-icons">delete_outline</Icon>&nbsp;
								<span class="text-xs">Remove</span>
							</div>
						</Content>
					</Paper>
				</div>
			{/if}
			{#await result then res}
				{#if res !== null}
					<span style:margin-right="10px">
						{res.metric !== undefined ? res.metric.toFixed(2) : ''}
					</span>
					<span class="italic text-grey-darker mr-2.5">
						({res.size.toLocaleString()})
					</span>
				{/if}
			{/await}
			{#if $editTag === undefined || $editTag.id !== tag.id}
				<div class="flex">
					<div
						style:width="36px"
						use:clickOutside={() => {
							hovering = false;
						}}
					>
						{#if hovering}
							<IconButton
								size="button"
								style="padding: 0px"
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
				</div>
			{/if}
		</div>
	</div>
</button>
