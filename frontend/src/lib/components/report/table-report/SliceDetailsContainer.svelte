<script lang="ts">
	import SliceDetails from '$lib/components/general/SliceDetails.svelte';
	import { selections } from '$lib/stores';
	import type { Slice } from '$lib/zenoapi';

	export let sli: Slice | undefined;

	let showTooltip = false;
</script>

{#if sli !== undefined}
	<div
		class="slice-link"
		on:click={() => {
			// TODO: navigate to explore Tab
			selections.update((sel) => ({
				slices: sli !== undefined && sli.sliceName !== 'All Instances' ? [sli.id] : [],
				metadata: sel.metadata,
				tags: sel.tags
			}));
		}}
		on:mouseover={() => (showTooltip = true)}
		on:mouseout={() => (showTooltip = false)}
		on:focus={() => (showTooltip = true)}
		on:blur={() => (showTooltip = false)}
		on:keydown={() => ({})}
	>
		{sli.sliceName}
	</div>
	{#if sli.sliceName !== 'All Instances' && showTooltip}
		<div class="tooltip-container">
			<div class="tooltip">
				<SliceDetails predicateGroup={sli.filterPredicates} />
			</div>
		</div>
	{/if}
{/if}

<style>
	.tooltip-container {
		z-index: 10;
		width: fit-content;
		position: absolute;
		transform: translateY(10%);
	}
	.tooltip {
		background: var(--G6);
		padding-left: 10px;
		padding-right: 10px;
		box-shadow: 1px 1px 3px 1px var(--G3);
		border-radius: 4px;
		padding-top: 10px;
		padding-bottom: 10px;
	}
	.slice-link {
		color: #6a1b9a;
		cursor: pointer;
	}
</style>
