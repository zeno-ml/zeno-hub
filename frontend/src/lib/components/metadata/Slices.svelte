<script lang="ts">
	import { comparisonModel, model } from '$lib/stores';
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
		class="flex items-center border border-grey-lighter rounded px-2.5 justify-between cursor-pointer text-grey w-full h-9
			{$selectionPredicates === undefined ? 'bg-primary-light' : ''}
			{$page.url.href.includes('compare') ? 'py-1' : ''}"
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
				<div style:width="36px" />
			</div>
		{/if}
	</button>
	{#each $folders as folder}
		<FolderCell {folder} />
	{/each}
	{#each $slices.filter((s) => s.folderId === null && s.sliceName !== 'All Instances') as s (s.sliceName)}
		<SliceCell compare={$page.url.href.includes('compare')} slice={s} />
	{/each}
</div>
