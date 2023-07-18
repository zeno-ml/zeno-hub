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
<div
	class="overview
			{$selectionPredicates === undefined ? 'selected' : ''}
			{$page.url.href.includes('compare') ? 'compare-slice-cell' : ''}"
	on:keydown={() => ({})}
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
	<div class="inline">All instances</div>
	{#if $model}
		<div class="inline">
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
</div>
{#each $folders as folder}
	<FolderCell {folder} />
{/each}
{#each $slices.filter((s) => s.folderId === null && s.sliceName !== 'All Instances') as s (s.sliceName)}
	<SliceCell compare={$page.url.href.includes('compare')} slice={s} />
{/each}

<style>
	.inline {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
	.compare-slice-cell {
		padding-top: 5px;
		padding-bottom: 5px;
	}
	.overview {
		display: flex;
		align-items: center;
		border: 1px solid var(--G5);
		border-radius: 4px;
		padding-left: 10px;
		justify-content: space-between;
		padding-right: 10px;
		min-height: 36px;
		cursor: pointer;
		color: var(--G1);
	}
	.selected {
		background: var(--P3);
	}
</style>
