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

<div
	class="{inFolder ? 'in-folder' : ''} cell parent {selected ? 'selected' : ''}"
	on:click={setSelected}
	draggable="true"
	on:mouseover={() => (hovering = true)}
	on:focus={() => (hovering = true)}
	on:mouseleave={() => (hovering = false)}
	on:blur={() => (hovering = false)}
	on:dragstart={dragStart}
	on:keydown={() => ({})}
>
	<div class="group" style:width="100%">
		<div class="group" style:width="100%">
			<div class="inline">
				<div class="group" style:color="var(--G1)">
					{tag.tagName}
				</div>
			</div>
			<div
				class="group"
				use:clickOutside={() => {
					showOptions = false;
				}}
			>
				{#if showOptions}
					<div id="options-container">
						<Paper style="padding: 3px 0px;" elevation={7}>
							<Content>
								{#if $editTag === undefined}
									<div
										class="option"
										on:keydown={() => ({})}
										on:click={(e) => {
											e.stopPropagation();
											showOptions = false;
											editTag.set(tag);
										}}
									>
										<Icon style="font-size: 18px;" class="material-icons">edit</Icon>&nbsp;
										<span>Edit</span>
									</div>
								{/if}
								<div
									class="option"
									on:keydown={() => ({})}
									on:click={(e) => {
										e.stopPropagation();
										showOptions = false;
										removeTag();
									}}
								>
									<Icon style="font-size: 18px;" class="material-icons">delete_outline</Icon>&nbsp;
									<span>Remove</span>
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
						<span id="size">
							({res.size.toLocaleString()})
						</span>
					{/if}
				{/await}
				{#if $editTag === undefined || $editTag.id !== tag.id}
					<div class="inline" style:cursor="pointer">
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
	</div>
</div>

<style>
	#size {
		font-style: italic;
		color: var(--G3);
		margin-right: 10px;
	}
	.cell {
		position: relative;
		overflow: visible;
		border: 0.5px solid var(--G4);
		border-radius: 15px;
		margin-top: 5px;
		display: flex;
		padding-left: 10px;
		padding-right: 10px;
		min-height: 36px;
	}
	.group {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
		cursor: pointer;
	}
	.selected {
		background: var(--N2);
	}
	.inline {
		display: flex;
		flex-direction: row;
	}
	.in-folder {
		margin-left: 35px;
		margin-top: 0px;
		margin-bottom: 0px;
	}
	#options-container {
		top: 0px;
		right: 0px;
		z-index: 5;
		position: absolute;
		margin-top: 35px;
	}
	.option {
		display: flex;
		flex-direction: row;
		align-items: center;
		cursor: pointer;
		width: 73px;
		padding: 1px 6px;
	}
	.option span {
		font-size: 12px;
	}
	.option:hover {
		background: var(--G5);
	}
</style>
