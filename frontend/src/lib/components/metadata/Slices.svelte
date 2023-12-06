<script lang="ts">
	import { comparisonModel, model, project } from '$lib/stores';
	import { Join } from '$lib/zenoapi';

	import { folders, selectionPredicates, selections, slices, tagIds } from '$lib/stores';

	import { page } from '$app/stores';
	import SliceHeader from './SliceHeader.svelte';
	import FolderCell from './cells/FolderCell.svelte';
	import SliceCell from './cells/SliceCell.svelte';
	import SliceCellResult from './cells/SliceCellResult.svelte';
</script>

<SliceHeader />
<div class="mb-2">
	<button
		class="flex w-full cursor-pointer items-center justify-between rounded border border-grey-lighter px-2.5 text-grey
			{$selectionPredicates === undefined ? 'bg-primary-light' : ''}
			{$page.url.href.includes('compare') ? 'h-11 py-1' : 'h-9'}"
		on:click={() => {
			selections.update((m) => {
				Object.keys(m.metadata).forEach((key) => {
					m.metadata[key] = { predicates: [], join: Join._ };
				});
				return { slices: [], metadata: { ...m.metadata }, tags: [] };
			});
			tagIds.set(undefined);
		}}
	>
		<span>All instances</span>
		{#if $model}
			<div class="flex items-center justify-between">
				<SliceCellResult
					compare={$page.url.href.includes('compare')}
					slice={{
						id: -1,
						sliceName: '',
						folderId: undefined,
						filterPredicates: { predicates: [], join: Join._ }
					}}
					sliceModel={$model}
				/>
				{#if $page.url.href.includes('compare') && $comparisonModel}
					<SliceCellResult
						compare={true}
						slice={{
							id: -1,
							sliceName: '',
							folderId: undefined,
							filterPredicates: { predicates: [], join: Join._ }
						}}
						sliceModel={$comparisonModel}
					/>
				{/if}
				{#if $project.editor}
					<div style:width="36px" />
				{/if}
			</div>
		{/if}
	</button>
	{#each $folders as folder}
		<FolderCell {folder} />
	{/each}
	{#each $slices.filter((s) => s.folderId === null || s.folderId === undefined) as s (s.id)}
		<SliceCell compare={$page.url.href.includes('compare')} slice={s} />
	{/each}
</div>
