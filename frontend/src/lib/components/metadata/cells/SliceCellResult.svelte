<script lang="ts">
	import { metric, selections } from '$lib/stores';
	import { getMetricsForSlices, doesModelDependOnPredicates } from '$lib/api/slice';
	import type { Slice } from '$lib/zenoapi';

	export let compare: boolean;
	export let slice: Slice;
	export let sliceModel: string;

	$: compareButton = doesModelDependOnPredicates(slice.filterPredicates.predicates);
	$: selected = $selections.slices.includes(slice.id);
	$: compareButtonstyle = compareButton ? 'compare-btn ' + (selected ? 'selected' : '') : '';
</script>

{#if $metric}
	{#await getMetricsForSlices([{ slice: slice, model: sliceModel, metric: $metric }]) then res}
		{#if res !== null}
			<div class={compare ? 'compare ' + compareButtonstyle : 'flex-row'} on:keydown={() => ({})}>
				<span>
					{res[0].metric !== undefined && res[0].metric !== null ? res[0].metric.toFixed(2) : ''}
				</span>
				<span class="size">
					({res[0].size.toLocaleString()})
				</span>
			</div>
		{/if}
	{/await}
{/if}

<style>
	.flex-row {
		display: flex;
		align-items: center;
	}
	span {
		width: 50px;
		margin-right: 5px;
		text-align: right;
	}
	.size {
		font-style: italic;
		color: var(--G3);
	}
	.compare {
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-right: 10px;
		padding: 1px;
	}
	.compare-btn {
		border: 0.5px solid var(--G4);
		border-radius: 5px;
	}
	.compare-btn:hover {
		cursor: pointer;
		box-shadow: 0px 1px 2px 0px var(--G4);
	}
	.selected {
		background: var(--P3);
	}
</style>
